from __future__ import annotations

import json
import os
import time
from typing import List, Optional

from openai import OpenAI

from app.models.news_item import NewsItem


class AISummaryService:
    """
    使用豆包（火山方舟）对最终有效资讯进行标题与摘要标准化，并补充全球AI产业动态的归属/重点事件判断。

    建议放在：
    数据库去重后 -> 调用本服务 -> 导出 Excel / Word
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "doubao-seed-2-0-mini-260215",
        base_url: str = "https://ark.cn-beijing.volces.com/api/v3",
        max_retries: int = 2,
        retry_sleep_seconds: float = 1.5,
    ) -> None:
        self.api_key = api_key or os.getenv("ARK_API_KEY")
        if not self.api_key:
            raise ValueError("未提供方舟 API Key，请配置 ARK_API_KEY 环境变量或传入 api_key")

        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key,
        )
        self.model = model
        self.max_retries = max_retries
        self.retry_sleep_seconds = retry_sleep_seconds

    def process_items(self, items: List[NewsItem]) -> List[NewsItem]:
        result: List[NewsItem] = []
        for idx, item in enumerate(items, start=1):
            print(f"[AISummaryService] processing {idx}/{len(items)}")
            result.append(self.process_item(item))
        return result

    def process_item(self, item: NewsItem) -> NewsItem:
        prompt_text = self._build_input_content(item)
        if not prompt_text.strip():
            item.remarks = self._append_remark(item.remarks, "AI摘要跳过：缺少可用正文")
            self._fill_default_global_fields(item)
            return item

        data = self._call_model_with_retry(prompt_text)

        if not data:
            item.remarks = self._append_remark(item.remarks, "AI摘要失败，保留原标题摘要")
            self._fill_default_global_fields(item)
            return item

        ai_title = self._safe_str(data.get("title"))
        ai_summary = self._safe_str(data.get("summary"))
        ai_region_label = self._safe_str(data.get("global_region_label"))
        ai_key_flag = self._safe_str(data.get("global_key_event_flag"))
        ai_key_reason = self._safe_str(data.get("global_key_event_reason"))

        try:
            ai_key_score = int(data.get("global_key_event_score", 0))
        except Exception:
            ai_key_score = 0

        # 双保险：摘要最长100字
        if ai_summary and len(ai_summary) > 120:
            ai_summary = ai_summary[:120].rstrip()

        # 写回标题、摘要
        if ai_title:
            item.title_zh = ai_title
            item.title = ai_title

        if ai_summary:
            item.summary_zh = ai_summary
            item.summary = ai_summary

        # 注意：不覆盖 cleaned_content / original_cleaned_content
        # 这样能保留抓到的详细正文，供后续排查或再次处理使用

        # 写回全球AI产业动态的归属判断
        if ai_region_label in {"国内", "国际", "不适用"}:
            item.global_region_label = ai_region_label
        else:
            item.global_region_label = "不适用"

        # 写回重点事件判断
        if ai_key_flag in {"是", "否", "不适用"}:
            item.global_key_event_flag = ai_key_flag
        else:
            item.global_key_event_flag = "不适用"

        item.global_key_event_score = max(0, min(ai_key_score, 100))
        item.global_key_event_reason = ai_key_reason if ai_key_reason else "不适用"

        item.remarks = self._append_remark(item.remarks, "已使用豆包重写标题与摘要")
        return item

    def _call_model_with_retry(self, prompt_text: str) -> Optional[dict]:
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": prompt_text,
                                }
                            ],
                        }
                    ],
                )

                text = getattr(response, "output_text", "") or ""
                text = text.strip()

                if text.startswith("```"):
                    text = text.strip("`")
                    text = text.replace("json", "", 1).strip()

                data = json.loads(text)

                if not isinstance(data, dict):
                    raise ValueError("模型返回不是对象")

                required_fields = {
                    "title",
                    "summary",
                    "global_region_label",
                    "global_key_event_flag",
                    "global_key_event_score",
                    "global_key_event_reason",
                }
                missing = required_fields - set(data.keys())
                if missing:
                    raise ValueError(f"模型返回缺少字段: {sorted(missing)}")

                return data

            except Exception as e:
                last_error = e
                print(f"[AISummaryService] attempt={attempt + 1} failed: {repr(e)}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_sleep_seconds)

        print(f"[AISummaryService] all retries failed: {repr(last_error)}")
        return None

    @staticmethod
    def _build_input_content(item: NewsItem) -> str:
        company_text = "、".join(item.related_companies) if item.related_companies else "未识别"
        title_text = item.original_title or item.title or ""
        summary_text = item.original_summary or item.summary or ""

        # 优先选择更长、更完整的正文
        detail_candidates = [
            item.original_cleaned_content or "",
            item.raw_content or "",
            item.cleaned_content_zh or "",
            item.cleaned_content or "",
            item.summary_zh or "",
            item.summary or "",
        ]
        detail_text = max(detail_candidates, key=lambda x: len(str(x or "").strip()))
        detail_text = str(detail_text or "").strip()

        return (
            "请严格依据以下资讯内容生成结果，不得补充外部信息，不得猜测。\n"
            "请只返回 JSON，不要返回其他说明文字。\n"
            'JSON格式：{"title":"中文标题","summary":"中文摘要（目标80字左右）","global_region_label":"国内/国际/不适用","global_key_event_flag":"是/否/不适用","global_key_event_score":0,"global_key_event_reason":"简短理由"}\n'
            "要求：\n"
            "1. 优先依据“详细资讯内容”总结，不要只改写原标题或原摘要；\n"
            "2. title：中文标题，准确、简洁，只聚焦一个核心事件；\n"
            "3. summary：中文摘要，目标80个汉字左右，允许范围60-110个汉字，要把事情讲清楚，包含核心事实要素（谁/做了什么/关键结果），要把句子说全，以句号结束，禁止空泛套话（如“引发关注”“意义重大”），不要罗列无关背景；\n"
            "4. summary:中文摘要请体现本条资讯与关联企业有什么关系；\n"
            "5. global_region_label：仅当一级类别为“全球AI产业动态”时判断该资讯主体属于“国内”还是“国际”；\n"
            "6. 若主体属于中国境内机构、国内企业、国内高校、国内科研院所、国内政府部门，则标记为“国内”；\n"
            "7. 若主体属于国外企业、国外机构、国际组织、外国政府部门，则标记为“国际”；\n"
            "8. 若该条资讯不是“全球AI产业动态”，则 global_region_label 填“不适用”；\n"
            "9. 对于“全球AI产业动态”，请再从“机构全球知名度”“事件产业影响力”两个维度综合判断，是否属于重点事件；\n"
            "10. global_key_event_flag：若是全球AI产业动态中的重点事件，填“是”，否则填“否”；若不是全球AI产业动态，填“不适用”；\n"
            "11. global_key_event_score：0-100分，分数越高表示越值得列为重点事件；若不是全球AI产业动态，填0；\n"
            "12. global_key_event_reason：用一句简短中文说明判断理由；若不是全球AI产业动态，填“不适用”；\n"
            "13. 重点事件优先考虑：全球知名企业/组织/高校/院所的重要动作，或对AI产业链、资本市场、政策监管、技术路线产生明显影响的事件；\n"
            "14. 只能依据我提供的内容。\n\n"
            f"关联企业：{company_text}\n"
            f"一级类别：{item.category_level_1 or ''}\n"
            f"二级类别：{item.category_level_2 or ''}\n"
            f"原标题：{title_text}\n"
            f"原摘要：{summary_text}\n"
            f"详细资讯内容：{detail_text}"
        ).strip()

    @staticmethod
    def _fill_default_global_fields(item: NewsItem) -> None:
        if not item.global_region_label:
            item.global_region_label = "不适用"
        if not item.global_key_event_flag:
            item.global_key_event_flag = "不适用"
        if item.global_key_event_score is None:
            item.global_key_event_score = 0
        if not item.global_key_event_reason:
            item.global_key_event_reason = "不适用"

    @staticmethod
    def _safe_str(value) -> str:
        if value is None:
            return ""
        return str(value).strip()

    @staticmethod
    def _append_remark(existing: str | None, new_text: str) -> str:
        if not existing:
            return new_text
        return f"{existing}；{new_text}"