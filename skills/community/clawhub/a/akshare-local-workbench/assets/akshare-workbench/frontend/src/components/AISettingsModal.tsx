import { useEffect, useState } from "react";

import { getAIConfig, saveAIConfig } from "../services/api";
import type { AIConfigPublic } from "../types";

interface AISettingsModalProps {
  onClose: () => void;
  onSaved: (config: AIConfigPublic) => void;
}

const PRESETS = [
  { label: "OpenAI", base_url: "https://api.openai.com/v1", model: "gpt-4o-mini" },
  { label: "DeepSeek", base_url: "https://api.deepseek.com/v1", model: "deepseek-chat" },
  { label: "通义千问", base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1", model: "qwen-plus" },
  { label: "智谱 GLM", base_url: "https://open.bigmodel.cn/api/paas/v4", model: "glm-4-flash" },
  { label: "本地 Ollama", base_url: "http://127.0.0.1:11434/v1", model: "qwen2.5" }
];

export function AISettingsModal({ onClose, onSaved }: AISettingsModalProps) {
  const [baseUrl, setBaseUrl] = useState("");
  const [model, setModel] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [hasKey, setHasKey] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAIConfig()
      .then((cfg) => {
        setBaseUrl(cfg.base_url);
        setModel(cfg.model);
        setHasKey(cfg.has_key);
      })
      .catch(() => undefined);
  }, []);

  async function handleSave() {
    if (!baseUrl.trim() || !model.trim()) {
      setError("请填写 Base URL 和模型名称。");
      return;
    }
    if (!apiKey.trim() && !hasKey) {
      setError("请填写 API Key。");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      // Empty api_key means "keep the existing key" on the backend.
      const saved = await saveAIConfig({
        base_url: baseUrl.trim(),
        model: model.trim(),
        api_key: apiKey.trim()
      });
      onSaved(saved);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "保存失败");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-head">
          <h3>配置 AI 模型</h3>
          <button type="button" className="modal-close" onClick={onClose} aria-label="关闭">
            ×
          </button>
        </div>

        <p className="modal-hint">
          兼容 OpenAI 协议的任意服务。配置保存在本机后端，一次配置后长期有效。
        </p>

        <div className="preset-row">
          {PRESETS.map((preset) => (
            <button
              key={preset.label}
              type="button"
              className="preset-pill"
              onClick={() => {
                setBaseUrl(preset.base_url);
                setModel(preset.model);
              }}
            >
              {preset.label}
            </button>
          ))}
        </div>

        <label className="field">
          <span>Base URL</span>
          <input
            type="text"
            value={baseUrl}
            placeholder="https://api.deepseek.com/v1"
            onChange={(e) => setBaseUrl(e.target.value)}
          />
        </label>

        <label className="field">
          <span>模型名称</span>
          <input
            type="text"
            value={model}
            placeholder="deepseek-chat"
            onChange={(e) => setModel(e.target.value)}
          />
        </label>

        <label className="field">
          <span>API Key</span>
          <input
            type="password"
            value={apiKey}
            placeholder={hasKey ? "已配置（如需修改请重新输入）" : "sk-..."}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </label>

        {error && <div className="error-banner">{error}</div>}

        <div className="modal-actions">
          <button type="button" className="ghost-button" onClick={onClose}>
            取消
          </button>
          <button
            type="button"
            className="primary-button"
            disabled={saving}
            onClick={handleSave}
          >
            {saving ? "保存中…" : "保存配置"}
          </button>
        </div>
      </div>
    </div>
  );
}
