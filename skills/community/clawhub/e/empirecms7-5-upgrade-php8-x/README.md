# EmpireCMS 7.5 PHP 8 升级技能

将帝国CMS 7.5 站点升级到完全兼容 PHP 8.x 的专业技能包。

## 功能概述

- 按 P0→P1→P2 优先级逐文件执行 30 余项 PHP 8 兼容性修复
- 覆盖 connect.php、数组键引号、count() 替换、each()→foreach、preg_replace /e、create_function、split、字符串比较等核心改动
- 输出修改汇总和验证测试建议

## 变更日志

### v1.0.2 (2026-07-02)
- 新增 Init-Step-Poll 渐进式防卡死协议
- 长任务升级按 Init 建队列、Step 单文件修复、Poll 查询进度执行
- 明确未验证文件不得计入完成度，支持从最后一个已验证文件恢复

### v1.0.1 (2026-06-19)
- 补充 version / author 字段
- 新增执行流程与约束规则章节
- 统一 sinfo 目录路径为 `e/admin/sinfo/`
- 标题去除「」措辞
- 新增边界矩阵章节

## 文件结构

```
empirecms7-php8-upgrade/
├── SKILL.md     # 主技能文件（执行流程、修改模板、约束规则）
└── README.md    # 本文件
```

## 使用方法

1. 在对话中引用本技能包路径
2. 提供帝国CMS 7.5 项目根目录
3. AI 助手将按 SKILL.md 中的执行流程逐步完成升级

## 版本

v1.0.2 — 2026-07-02
