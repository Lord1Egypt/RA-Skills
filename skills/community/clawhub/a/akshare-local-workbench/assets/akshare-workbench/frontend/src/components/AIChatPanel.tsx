import { useEffect, useRef, useState } from "react";

import { aiPlan, buildExportUrl, runExtraction } from "../services/api";
import type {
  AICandidate,
  AIChatMessage,
  ExportFormat,
  IndicatorParam,
  RunResponse
} from "../types";
import { truncateHistory } from "../utils/tokens";

import { CollectForm } from "./CollectForm";
import { DataPreview } from "./DataPreview";

interface AIChatPanelProps {
  configured: boolean;
  onOpenSettings: () => void;
}

type ChatStatus = "idle" | "thinking" | "fetching" | "success" | "error";

interface CollectSnapshot {
  indicatorName: string;
  form: IndicatorParam[];
  values: Record<string, string | number | boolean | null>;
}

interface DisplayMessage extends AIChatMessage {
  candidates?: AICandidate[];
  quickReplies?: string[];
  // A frozen, read-only copy of a parameter form the user already submitted.
  collectSnapshot?: CollectSnapshot;
}

interface CollectState {
  indicatorId: string;
  indicatorName: string;
  baseParams: Record<string, string | number | boolean | null>;
  form: IndicatorParam[];
}

const STATUS_LABEL: Record<ChatStatus, string> = {
  idle: "",
  thinking: "AI 正在理解你的需求…",
  fetching: "正在获取数据…",
  success: "数据已就绪",
  error: "处理失败"
};

const SUGGESTIONS = [
  "平安银行 2024 年日线行情",
  "最新的中国 CPI 月度数据",
  "贵州茅台最近一个月的日线",
  "沪深300 指数历史行情"
];

export function AIChatPanel({ configured, onOpenSettings }: AIChatPanelProps) {
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<ChatStatus>("idle");
  const [result, setResult] = useState<RunResponse | null>(null);
  const [collect, setCollect] = useState<CollectState | null>(null);
  const busy = status === "thinking" || status === "fetching";
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, status, collect]);

  function appendAssistant(
    content: string,
    candidates?: AICandidate[],
    quickReplies?: string[]
  ) {
    setMessages((prev) => [...prev, { role: "assistant", content, candidates, quickReplies }]);
  }

  async function runIndicator(
    indicatorId: string,
    indicatorName: string,
    params: Record<string, string | number | boolean | null>
  ) {
    setStatus("fetching");
    try {
      const run = await runExtraction(indicatorId, params);
      setResult(run);
      setStatus("success");
      appendAssistant(
        `已获取「${run.indicator_name}」共 ${run.row_count.toLocaleString("en-US")} 行数据，可在右侧预览并导出。`
      );
    } catch (err) {
      setStatus("error");
      appendAssistant(
        `「${indicatorName}」数据获取失败：${err instanceof Error ? err.message : "未知错误"}`
      );
    }
  }

  async function submit(text: string) {
    const trimmed = text.trim();
    if (!trimmed || busy) return;

    if (!configured) {
      setMessages((prev) => [
        ...prev,
        { role: "user", content: trimmed },
        {
          role: "assistant",
          content: "尚未配置 AI 模型，请先点击右上角「设置」填写模型 API。"
        }
      ]);
      setInput("");
      onOpenSettings();
      return;
    }

    const history: AIChatMessage[] = truncateHistory([
      ...messages.map(({ role, content }) => ({ role, content })),
      { role: "user", content: trimmed }
    ]);
    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setCollect(null);
    setStatus("thinking");

    try {
      const planResult = await aiPlan(history);

      if (planResult.action === "run" && planResult.indicator_id) {
        appendAssistant(planResult.reply);
        await runIndicator(
          planResult.indicator_id,
          planResult.indicator_name ?? planResult.indicator_id,
          planResult.params
        );
        return;
      }

      if (planResult.action === "collect" && planResult.indicator_id && planResult.form.length) {
        appendAssistant(planResult.reply);
        setCollect({
          indicatorId: planResult.indicator_id,
          indicatorName: planResult.indicator_name ?? planResult.indicator_id,
          baseParams: planResult.params,
          form: planResult.form
        });
        setStatus("idle");
        return;
      }

      // clarify / reject / error / not_configured
      appendAssistant(planResult.reply, planResult.candidates, planResult.quick_replies);
      setStatus(planResult.action === "error" ? "error" : "idle");
      if (planResult.action === "not_configured") onOpenSettings();
    } catch (err) {
      setStatus("error");
      appendAssistant(`AI 处理失败：${err instanceof Error ? err.message : "未知错误"}`);
    }
  }

  function submitCollect(values: Record<string, string | number | boolean | null>) {
    if (!collect || busy) return;
    const merged = { ...collect.baseParams, ...values };
    const { indicatorId, indicatorName, form } = collect;
    setCollect(null);
    // Keep the choices visible in the conversation as an inactive record
    // instead of removing the form from the dialog.
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: `好的，正在为你提取「${indicatorName}」…`,
        collectSnapshot: { indicatorName, form, values: merged }
      }
    ]);
    void runIndicator(indicatorId, indicatorName, merged);
  }

  function handleExport(format: ExportFormat) {
    if (!result) return;
    window.open(buildExportUrl(result.task_id, format), "_blank", "noopener,noreferrer");
  }

  function clearResult() {
    setResult(null);
    setStatus((prev) => (prev === "success" || prev === "error" ? "idle" : prev));
  }

  function startNewTask() {
    if (busy) return;
    setMessages([]);
    setInput("");
    setResult(null);
    setCollect(null);
    setStatus("idle");
  }

  return (
    <section className="ai-workspace">
      <div className="panel ai-chat-panel">
        <div className="ai-chat-head">
          <div>
            <p className="eyebrow">AI 智能取数</p>
            <h2>用自然语言描述你想要的数据</h2>
          </div>
          <div className="ai-head-actions">
            <button
              type="button"
              className="ghost-button ai-settings-btn"
              disabled={busy || (messages.length === 0 && !collect)}
              onClick={startNewTask}
            >
              ＋ 新任务
            </button>
            <button type="button" className="ghost-button ai-settings-btn" onClick={onOpenSettings}>
              ⚙ 设置
            </button>
          </div>
        </div>

        {!configured && (
          <div className="ai-config-hint">
            尚未配置 AI 模型，
            <button type="button" className="link-button" onClick={onOpenSettings}>
              点此配置 API
            </button>
            后即可使用。
          </div>
        )}

        <div className="ai-messages" ref={listRef}>
          {messages.length === 0 && (
            <div className="ai-empty">
              <p>试着这样问：</p>
              <div className="ai-suggestions">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    type="button"
                    className="ai-suggestion"
                    onClick={() => submit(s)}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, index) => {
            const isLast = index === messages.length - 1;
            const interactive = isLast && !busy && !collect;
            return (
              <div key={index} className={`ai-bubble ai-${msg.role}`}>
                <div className="ai-bubble-body">{msg.content}</div>
                {msg.collectSnapshot && (
                  <div className="ai-collect-record">
                    <CollectForm
                      indicatorName={msg.collectSnapshot.indicatorName}
                      form={msg.collectSnapshot.form}
                      baseParams={msg.collectSnapshot.values}
                      disabled
                    />
                  </div>
                )}
                {msg.quickReplies && msg.quickReplies.length > 0 && (
                  <div className="ai-quick-replies">
                    {msg.quickReplies.map((q) => (
                      <button
                        key={q}
                        type="button"
                        className="ai-quick-reply"
                        disabled={!interactive}
                        onClick={() => submit(q)}
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                )}
                {msg.candidates && msg.candidates.length > 0 && (
                  <div className="ai-candidates">
                    {msg.candidates.map((c) => (
                      <button
                        key={c.id}
                        type="button"
                        className="ai-candidate"
                        disabled={!interactive}
                        onClick={() => submit(`我要「${c.name}」`)}
                      >
                        {c.name}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            );
          })}

          {collect && !busy && (
            <CollectForm
              key={`${collect.indicatorId}-${collect.form.map((f) => f.name).join(",")}`}
              indicatorName={collect.indicatorName}
              form={collect.form}
              baseParams={collect.baseParams}
              onSubmit={submitCollect}
            />
          )}

          {busy && (
            <div className="ai-bubble ai-assistant">
              <div className="ai-status">
                <span className="ai-spinner" />
                {STATUS_LABEL[status]}
              </div>
            </div>
          )}
        </div>

        <form
          className="ai-input-row"
          onSubmit={(e) => {
            e.preventDefault();
            submit(input);
          }}
        >
          <input
            type="text"
            className="ai-input"
            value={input}
            disabled={busy}
            placeholder={configured ? "例如：平安银行 2024 年日线行情" : "请先配置 AI 模型…"}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" className="primary-button" disabled={busy || !input.trim()}>
            发送
          </button>
        </form>
      </div>

      <div className="ai-preview">
        <DataPreview
          result={result}
          status={status === "fetching" ? "fetching" : "idle"}
          onExport={handleExport}
          onClear={clearResult}
        />
      </div>
    </section>
  );
}
