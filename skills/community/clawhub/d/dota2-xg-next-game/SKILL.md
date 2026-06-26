---
name: "dota2 XG next game"
description: "查询 Xtreme Gaming (XG) 战队的下一场比赛信息。通过 Liquipedia API 获取精准、实时的赛程数据。当用户询问 XG 何时有比赛或下一场对手是谁时调用。"
author: "ame hater"
version: "1.1.0"
metadata: { "openclaw": { "requires": { "bins": ["curl", "jq"] } } }
---

# dota2 XG next game (API Edition)

这个技能通过 **Liquipedia MediaWiki API** 接口直接获取 Xtreme Gaming (XG) 的赛程数据，完美绕过前端页面的反爬限制（403 Forbidden）和代理环境（TUN 模式）下的 SSRF 拦截。

## 运行逻辑
1. **API 抓取 (核心)**：
   - **指令**：使用 `RunCommand` 执行以下 `curl` 命令（必须带 User-Agent）：
     `curl -H "User-Agent: Trae/1.0 (OpenClaw Skill)" -s "https://liquipedia.net/dota2/api.php?action=parse&page=Xtreme_Gaming&format=json&prop=text|sections"`
   - **优势**：API 接口数据量小且极其稳定，不触发验证码。
2. **解析 JSON 数据**：
   - 在返回的 JSON 中查找 `sections` 列表，定位到 `anchor` 为 `Upcoming_Matches` 的 `index`（通常在末尾）。
   - 根据该 `index` 提取对应的 `text` 内容。
3. **深入分析赛程阶段**：
   - 从提取的内容中识别下一场比赛所在的赛事（Tournament）。
   - 如果需要进一步确认赛事轮次（如败者组 Lower Bracket），可对该赛事页面再次调用 API。
4. **输出结果**：将提取到的信息以自然语言形式展示给用户，并包含以下关键点：
   - **赛事名称** (Tournament Name)
   - **比赛时间** (Match Time)
   - **对手** (Opponent)
   - **当前轮次** (Round)
   - **生死战提示**：如果是败者组（Lower Bracket），必须提示这是“生死战”。
   - **特别彩蛋**：如果是生死战，必须输出“输了ame就回家啦🤣”。

## 输出风格 (LLM 优化)
- **自然语言**：严禁直接打印原始 JSON。使用口语化、像在哥们儿聊天一样的语气来总结比赛信息。
- **态度鲜明**：保持 "ame hater" 的设定。在提及 Ame 的表现或潜在后果时，可以带点调侃、恨铁不成钢、或准备看戏的语气。
- **关键信息加粗**：将时间、对手、赛制（如 Bo3）和轮次加粗。

## 使用场景
- 当用户询问 "XG 下一场打谁？"、"XG 什么时候有比赛？"、"XG 赛程" 等与未来比赛相关的话题时。

## 注意事项
- **时区转换**：Liquipedia 原始数据通常为 UTC，必须手动换算为北京时间（CST, UTC+8）。
- **无赛程处理**：如果 API 返回中找不到 `Upcoming_Matches` 节点，说明该战队目前没有已公开的未来赛程。
- **解析效率**：API 返回的内容比 HTML 干净得多，Agent 应当利用这种结构化优势进行精准提取。
- **保持人设**：不要忘了作者是 "ame hater"，在输出最后记得加上彩蛋。
