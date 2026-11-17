# ADR — cite-holmes 架构决策记录（公开层）

> 记录「做了什么决定 + 为什么」。每条满足三条件才在案：难逆转、缺上下文会困惑、
> 存在真实权衡。一段话也是合法 ADR——价值在决策本身，不在篇幅。
> 旁边的归档体系（会话笔记/内部台账）不在仓库内；这里只放对使用者与贡献者
> 有意义的公开工程决策。

| ADR | 决策 | 状态 |
|---|---|---|
| [ADR-0001](0001-verdict-contract.md) | 判定契约：adjust ∈ 三值，一致=空串 | Accepted |
| [ADR-0002](0002-circuit-breaker-transport-only.md) | 断路器只记传输层失败 | Accepted |
| [ADR-0003](0003-offline-caps-partial.md) | offline 封顶 partial，绝不判 verified | Accepted |
| [ADR-0004](0004-cross-lingual-never-fabrication-evidence.md) | 跨语言差异永不作为编造依据 | Accepted |
| [ADR-0005](0005-signals-annotate-never-verdicts.md) | 线索信号只注记，绝不改判定 | Accepted |
| [ADR-0006](0006-single-way-github-mirror.md) | GitHub 单向镜像，trunk 是唯一真相源 | Accepted |
| [ADR-0007](0007-neutral-language-in-published-files.md) | 官方文件只写能力与价值，不写对号入座的应试表述 | Accepted |
