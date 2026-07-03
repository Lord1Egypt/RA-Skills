# Article Tuwen — 完整执行流程

详细4 Phase执行规范。SKILL.md只保留规则和格式，本文件是执行引擎。

---

## Phase 1: 素材摄入 & 长文撰写

### 1.1 素材获取
- URL → WebFetch抓取全文
- 文件路径 → Read读取
- 粘贴文本 → 直接使用
- 多素材按顺序阅读，合并信息

### 1.2 长文撰写
- 字数：3500-4500字
- 结构：标题(含核心关键词) → 导语 → 4-6章节 → 结语
- 标题必须包含素材核心产品/技术名
- 每章必须有具体数据、原话引述、技术细节
- 保留原文「」原话和数据
- 保存为 `<slug>-article.md`

---

## Phase 2: 去重多样性检查

### 2.1 读取历史
- 读取 `history.json`（同目录下）
- 不存在或损坏则从空状态开始

### 2.2 轮换池

| 维度 | 池 |
|------|-----|
| 封面搜索词 | server room, data center, abstract blue, technology hands, neural network, code screen, circuit board, city skyline night |
| 封底搜索词 | abstract dark, night city, deep space, dark ocean, sunset silhouette, mountain fog, rain window, dark forest |
| Editorial主题 | indigo-porcelain, ink-classic, kraft-paper, arctic-dawn, moss-stone |
| Swiss主题 | copper-oxide, slate-storm, sage-garden, wine-dark-sea, desert-rose |

### 2.3 约束规则
- 封面/封底/主题按索引轮换，与最近3次不同
- 布局序列首尾固定(M01/M02开头，M15/M16结尾)，中间不与上次前3个重复
- 有数据场景时使用C01-C10图表，与上次不同

---

## Phase 3: 排版渲染

### 3.1 品类推断
- 商业/科技/分析 → Editorial
- 职场/干货/教程 → Swiss

### 3.2 内容规划
- 3500-4500字 → 8-9页
- 至少5种不同版式形态
- 标注明暗/氛围/版式节奏

### 3.3 组装HTML
- 拷贝种子模板（xhs-crafter的assets/目录）
- 注入Phase 2多样性约束
- 下载封面/封底图片到本地assets/
- 遵循字号铁律、密度铁律、关键词铁律

### 3.4 自检自修复
- 字号：搜索inline font-size，发现即替换为class
- 密度：每页≥78%，不足追加内容
- 关键词：核心词每页至少1处
- 图片：无broken image
- 节奏：暗色页不相邻，版式不重复

### 3.5 截图（关键步骤！）
1. **杀掉所有python进程**：`Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force`
2. **cd到当前项目目录**
3. 启动HTTP服务器：`python -m http.server 8090`
4. 等待3秒
5. 运行screenshot.js
6. **验证**：对比新截图文件大小与上次，完全一致说明服务器指向错误

### 3.6 文字稿
- 模板：标题(1句)→场景开场(2句)→核心论点(2句)→关键原话(2条「」)→数据(5个)→结尾原话(1条)
- 字数：≥800且≤1000字
- 保存为 `<slug>-文字稿.txt`

---

## Phase 4: 交付 & 记录

### 4.1 本地交付
- `Start-Process xcopy` 复制到 `C:\Users\Administrator\Desktop\<slug>公众号配图\`
- `explorer.exe` 打开文件夹

### 4.2 飞书云盘
- `lark-cli drive +create-folder --name "<slug>公众号配图"`
- cd到output目录后逐个上传（lark-cli要求相对路径）
- 返回飞书URL

### 4.3 更新history.json
- 追加本次运行记录
- 更新轮换索引
- 保存

---

## 异常处理

| 异常 | 处理 |
|------|------|
| URL抓取失败 | 重试1次，仍失败提示用户提供文本 |
| 素材<500字 | 提示"素材过少"但继续执行 |
| 图片下载失败 | 重试3次，失败切换图源 |
| 桌面路径权限 | 用Start-Process xcopy绕行 |
| 飞书token过期 | 重新创建文件夹 |
| history.json损坏 | 从空状态开始 |
| 截图内容错误 | 杀进程→确认目录→重启服务器→重截图 |
