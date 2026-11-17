# 参考：文档体系规范

> 来源：阮一峰《中文技术文档写作规范 · 文档体系》

---

## 软件手册的推荐结构

软件手册是一部完整的书，建议采用以下结构。标注 **[必备]** 的章节必须存在，**[可选]** 的章节按需添加。

```
手册/
├── 简介（Introduction）         [必备] [文件]
├── 快速上手（Getting Started）   [可选] [文件]
├── 入门篇（Basics/使用篇）       [必备] [目录]
│   ├── 环境准备（Prerequisite）  [必备] [文件]
│   ├── 安装（Installation）      [可选] [文件]
│   └── 设置（Configuration）     [必备] [文件]
├── 进阶篇（Advanced/开发篇）     [可选] [目录]
├── API（Reference）              [可选] [目录|文件]
├── FAQ                           [可选] [文件]
└── 附录（Appendix）              [可选] [目录]
    ├── Glossary（名词解释）       [可选] [文件]
    ├── Recipes（最佳实践）        [可选] [文件]
    ├── Troubleshooting（故障处理）[可选] [文件]
    ├── ChangeLog（版本说明）      [可选] [文件]
    └── Feedback（反馈方式）       [可选] [文件]
```

### 各章节说明

| 章节 | 必备性 | 说明 |
|------|--------|------|
| **简介** | 必备 | 对产品和文档本身的总体、扼要说明 |
| **快速上手** | 可选 | 最快速使用产品的方式 |
| **入门篇** | 必备 | 提供初级使用教程的目录 |
| 环境准备 | 必备 | 使用软件需要满足的前置条件 |
| 安装 | 可选 | 软件的安装方法 |
| 设置 | 必备 | 软件的设置说明 |
| **进阶篇** | 可选 | 中高级开发教程 |
| **API** | 可选 | 软件 API 的逐一介绍 |
| **FAQ** | 可选 | 常见问题解答 |
| **附录** | 可选 | 对阅读教程有帮助但不属于教程本身的内容 |

### 参考范例

- [Redux 手册](https://redux.js.org/introduction/getting-started)
- [Atom 手册](http://flight-manual.atom.io/)

---

## 文件命名规范

### 规则 1：文件名不得含有空格

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| `getting started.md` | `getting-started.md` |
| `API Reference.md` | `api-reference.md` |

---

### 规则 2：文件名必须使用半角字符（不得使用中文）

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| `名词解释.md` | `glossary.md` |
| `安装说明.md` | `installation.md` |

---

### 规则 3：文件名建议只使用小写字母

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| `TroubleShooting.md` | `troubleshooting.md` |
| `GetStarted.md` | `get-started.md` |

**例外**：某些说明文件可以使用大写，如 `README`、`LICENSE`、`CHANGELOG`。

---

### 规则 4：多单词文件名用连词线（`-`）分隔

| ❌ 不佳 | ✅ 正确 |
|---------|---------|
| `advanced_usage.md`（下划线） | `advanced-usage.md` |
| `advancedusage.md`（无分隔） | `advanced-usage.md` |

---

## 文件命名速查

### 允许大写的文件名

```
README
README.md
LICENSE
CHANGELOG
CHANGELOG.md
CONTRIBUTING
CONTRIBUTING.md
```

### 常用文档文件名参考

| 中文含义 | 推荐文件名 |
|----------|-----------|
| 简介 | `introduction.md` |
| 快速上手 | `getting-started.md` |
| 安装 | `installation.md` |
| 配置/设置 | `configuration.md` |
| API 参考 | `api-reference.md` |
| 常见问题 | `faq.md` |
| 名词解释 | `glossary.md` |
| 最佳实践 | `recipes.md` |
| 故障排查 | `troubleshooting.md` |
| 版本说明 | `changelog.md` |

---

## 快速自查

- [ ] 文件名中无空格
- [ ] 文件名只使用半角字符（无中文）
- [ ] 文件名只使用小写字母（特殊说明文件除外）
- [ ] 多单词文件名使用 `-` 连接
- [ ] 文档包含必备章节：简介、入门篇（环境准备、设置）
- [ ] 章节结构清晰，层次合理
