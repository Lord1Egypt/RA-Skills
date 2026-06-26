---
name: arxiv-zotero-obsidian
description: |
  自动扫描 arxiv.drqyq.com 网站上的论文，更新到 Zotero 并生成阅读笔记。
  基于 zotero-mcp 和 obsidian skill 构建，自动获取收藏夹和 vault 信息。
---

# arxiv-zotero-obsidian Skill

这个技能可以自动扫描指定的 arxiv 论文分类页面，将相关论文添加到 Zotero 收藏夹，并生成深度阅读笔记到 Obsidian。

## 功能

1. **论文扫描**：访问 arxiv.drqyq.com 获取指定分类的最新论文
2. **Zotero 同步**：自动将新论文添加到指定的 Zotero 收藏夹（使用 zotero-mcp）
3. **Obsidian 集成**：自动获取 Obsidian vault 信息，写入阅读笔记

## 使用前配置

### 1. 获取 Zotero API Key

1. 访问 https://www.zotero.org/settings/api
2. 点击 "Create New Key"
3. 勾选以下权限：
   - **Library write**
   - **User library write**
4. 创建后记录 API Key

### 2. 配置示例

```
请配置并每天下午2点执行以下任务：
- Zotero API Key: 您的KEY
- 用户ID: 您的ID
- 扫描分类: PTA
- 目标收藏夹: Pending（会通过 zotero-mcp 自动查找）
- 笔记输出: DailyArXiv（会通过 obsidian skill 自动查找）
```

## 定时任务示例

```
每天下午2点：
1. 扫描 arxiv.drqyq.com/category/PTA/ 的论文
2. 通过 zotero-mcp 查询收藏夹，找到 "Pending" 收藏夹
3. 添加新论文到该收藏夹
4. 从收藏夹中选择论文进行深度阅读
5. 通过 obsidian skill 查找 vault，将笔记写入 DailyArXiv 文件夹
```

## 支持的分类

- **PTA**: 脉冲星计时阵列
- **GW**: 引力波
- **ML**: 机器学习
- **ASTRO**: 天体物理

## 技术细节

- **Zotero 集成**：使用 zotero-mcp skill 进行搜索和添加文献
- **Obsidian 集成**：使用 obsidian skill 查找 vault 和写入笔记
- **论文格式**：自动获取完整作者、摘要、DOI、PDF 链接
