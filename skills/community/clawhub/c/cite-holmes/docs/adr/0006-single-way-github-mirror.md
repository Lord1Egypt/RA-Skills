# ADR-0006: GitHub 单向镜像，trunk 是唯一真相源

日期: 2026-10-11 · 状态: Accepted

## 决策

GitHub 仓库是 trunk 的**单向镜像**（sync_github.sh 推送）；任何情况下不把
GitHub 上的改动合并回 trunk。

## 背景

镜像仓服务于发现与引用（GitHub 链接是学术用户的默认入口），trunk 服务于
开发。双向合并会引入"两边都是真相源"的漂移问题——发布一致性（版本号/
frontmatter/语言铁律）的断言链全部建立在单一真相源上。

## 后果

- 外部 PR/issue 的修复一律落 trunk 再镜像
- trunk 版本号与发布版本硬门校验（不一致大声失败）
