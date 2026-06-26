# 子能力映射

## 1. 下载 / 解析
来源：`douyin-copy-extractor`
脚本：`scripts/download_douyin.sh`

## 2. 错字稿修顺
来源：`transcript-polisher`
- 首选：`cpa/gpt-5.4`
- 备选：`cpa/claude-sonnet-4-6`

## 3. 结构拆解 / 钩子提炼 / 平台改写 / 仿写
来源：`script-analyzer`

## 主链提醒
固定顺序：
链接 → 转写 → 修顺 → 拆解 → 仿写

注意：
- 本 skill 不自建知识库
- 如果宿主本体有记忆/知识库能力，优先调用宿主能力
- 如果宿主没有，就只完成当前任务结果
