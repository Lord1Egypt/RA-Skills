#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""声明式适配器基类：用类属性描述「去哪找文件、怎么读消息、token 在哪」。

绝大多数新 Agent 的会话是 JSONL/JSON，只是目录和字段名不同。
子类只需声明类属性即可，无需重复写解析逻辑。

类属性：
  dir_patterns : 相对 home/appdata 的目录模式列表（支持单层 *）
  file_globs   : 文件名 glob 列表，如 ("*.jsonl", "context.jsonl")
  data_style   : "jsonl" | "json" | "json-array" | "flat-text"（每行一个纯文本）
  role_keys / user_values / text_keys : 覆盖默认字段（见 _jsonutil）
  token_spec   : dict(input=..., output=..., ...) 或 None（None=该 agent 不暴露 token）
  verified     : 是否用真实会话验证过（False 时报告标注「按公开格式编写，未验证」）
"""
import os
from .base import BaseAdapter, task, token, all_homes, appdata_roots
from ._jsonutil import (ROLE_KEYS, USER_VALUES, TEXT_KEYS, TOKEN_KEYS,
                        open_jsonl, open_json, as_text, is_user, message_text,
                        find_token, expand_dirs)


class DeclarativeAdapter(BaseAdapter):
    dir_patterns = ()
    file_globs = ("*.jsonl",)
    data_style = "jsonl"
    role_keys = ROLE_KEYS
    user_values = USER_VALUES
    text_keys = TEXT_KEYS
    token_spec = None          # 默认不暴露 token
    verified = False
    verification_note = ""

    def _roots(self):
        return expand_dirs(all_homes() + appdata_roots(), self.dir_patterns)

    def _files(self):
        seen, out = set(), []
        import glob
        for root in self._roots():
            for g in self.file_globs:
                for fp in glob.glob(os.path.join(root, g)):
                    if not os.path.isfile(fp):
                        continue
                    k = os.path.normcase(os.path.abspath(fp))
                    if k not in seen:
                        seen.add(k)
                        out.append(fp)
        return out

    def _records(self, fp):
        style = self.data_style
        if style == "jsonl":
            return open_jsonl(fp)
        if style == "json":
            d = open_json(fp)
            return [d] if d is not None else []
        if style == "json-array":
            d = open_json(fp)
            return d if isinstance(d, list) else []
        if style == "flat-text":
            out = []
            try:
                for line in open(fp, encoding="utf-8", errors="replace"):
                    line = line.strip()
                    if line:
                        out.append({"content": line, "role": "user"})
            except Exception:
                pass
            return out
        return []

    def _extract(self, obj):
        """返回 (user_text, record_for_token)；非用户消息返回 ('', None)。"""
        if isinstance(obj, str):
            return (obj, None)
        if not isinstance(obj, dict):
            return ("", None)
        if is_user(obj, self.role_keys, self.user_values):
            return (message_text(obj, self.text_keys), obj)
        # 无 role 字段但像用户消息（flat-text / user-history）
        if not any(k in obj for k in self.role_keys):
            if any(k in obj for k in self.text_keys):
                return (message_text(obj, self.text_keys), obj)
        return ("", None)

    def _sid(self, fp, i):
        return f"{self.name.lower()}-{os.path.basename(os.path.dirname(fp))}-{i}"

    def extract_tasks(self):
        from .base import pick_task
        rows = []
        for fp in self._files():
            cnt = 0
            for i, obj in enumerate(self._records(fp)):
                text, _ = self._extract(obj)
                text = (text or "").strip()
                if len(text) < 3:
                    continue
                t = pick_task([text])
                if not t:
                    continue
                cnt += 1
                rows.append(task(t[:80], t, self._sid(fp, i), "",
                                 os.path.dirname(fp), cnt,
                                 f"{self.name.lower()}-{self.data_style}", self.name))
        return rows

    def collect_tokens(self):
        if not self.token_spec:
            return []
        rows = []
        spec = self.token_spec  # dict: input/output/cache/total/model 各自的字段名覆盖
        for fp in self._files():
            for i, obj in enumerate(self._records(fp)):
                if not isinstance(obj, dict):
                    continue
                inp = self._tk(obj, "input", spec)
                out = self._tk(obj, "output", spec)
                if not (inp or out):
                    continue
                cache = self._tk(obj, "cache", spec)
                reason = self._tk(obj, "reason", spec)
                total = self._tk(obj, "total", spec) or (inp + out + cache)
                model = ""
                for k in spec.get("model", ()):
                    v = obj.get(k)
                    if isinstance(v, str):
                        model = v
                        break
                rows.append(token(self._sid(fp, i), "", "", "",
                                  os.path.dirname(fp), model,
                                  inp, out, cache, reason,
                                  source=f"{self.name.lower()}-{self.data_style}",
                                  total=total,
                                  fresh_rule="subtract" if cache else "add",
                                  agent=self.name))
        return rows

    def _tk(self, obj, group, spec):
        custom = spec.get(group)
        if custom:
            # 常见容器：顶层 / usage / tokens / usageMetadata（Gemini、Qwen）
            # / token_usage（Kimi wire）/ message.payload（Kimi StatusUpdate）
            msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
            containers = (obj, obj.get("usage"), obj.get("tokens"), obj.get("token_count"),
                          obj.get("usageMetadata"), obj.get("token_usage"),
                          msg.get("payload"))
            for k in custom:
                for container in containers:
                    if isinstance(container, dict) and isinstance(container.get(k), (int, float)):
                        return int(container[k])
        return find_token(obj, group, 0)

    def note(self):
        if self.token_available:
            return ""
        base = super().note()
        if self.verified:
            return base
        extra = self.verification_note or "按公开格式编写，本机未安装该 Agent，未用真实会话验证"
        return f"{base}；{extra}" if base else extra

    @property
    def token_available(self):
        return bool(self.token_spec)
