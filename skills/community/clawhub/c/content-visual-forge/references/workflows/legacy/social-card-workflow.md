# 社交平台组图完整流程

本文件描述小红书 / Rednote / 社交平台 3:4 组图的完整生成流程。

---

## 适用场景

- 小红书组图（4-8 页）
- Rednote 社交卡片
- Instagram Carousel
- 可滑动传播的视觉论证
- 产品介绍/工具推荐/避坑指南/对比评测

---

## 与 knowledge-carousel 的区别

| 维度 | knowledge-carousel | social-card |
|------|-------------------|-------------|
| **目标** | 讲清知识结构 | 形成传播性视觉论证 |
| **内容** | 方法论、教程、科普 | 产品更新、工具介绍、清单、对比、避坑 |
| **视觉** | 书卷感、编辑感 | 点击优先/保存优先/品牌优先 |
| **平台** | 通用 | 小红书/社交平台 |
| **规格** | 3:4 通用 | 1080×1440 平台规格 |

---

## 完整流程

### 阶段 0：Input Type Router

**参考：** [00-input-router.md](00-input-router.md)

识别输入源：
- 产品介绍文案
- 工具使用经验
- 避坑指南
- 对比评测
- 购买建议
- 使用教程

**输出：**
```md
输入源类型：产品介绍 / 经验分享 / 对比评测
可读取程度：完整 / 部分
下一步：Source Lock
```

---

### 阶段 1：Source Lock

**参考：** [01-source-lock.md](01-source-lock.md)

**必须回答：**
1. 内容真正讲什么产品/工具/方法？
2. 核心卖点/痛点是什么？
3. 目标用户是谁？
4. 传播角度是什么？（避坑/种草/对比/教程）
5. 有哪些视觉证据？（截图/产品图/对比图）

**输出：** Source Lock Report

**示例：**
```md
## Source Lock Report

### 内容源
类型：产品介绍文案
主题：XX 时间管理 App 使用体验
核心卖点：番茄钟 + 数据可视化 + 跨平台同步

### 目标用户
职场人士、学生党、需要时间管理工具的人

### 传播角度
种草 + 教程（展示功能 + 实际使用场景）

### 视觉证据
- App 界面截图（5 张）
- 数据统计界面
- 多设备同步效果图

### 建议分页
6 页（封面 + 痛点 + 功能亮点 3 页 + 使用场景 + 总结）

### 禁止偏离项
- 不得虚构产品没有的功能
- 不得使用其他 App 的截图
- 不得夸大效果
```

---

### 阶段 2：Output Mode Router

**参考：** [02-output-mode-router.md](02-output-mode-router.md)

**确认输出模式：** `social-card`

**判定依据：**
- 目标是小红书/社交平台组图 ✓
- 需要形成可滑动、可传播、可截图复用的视觉论证 ✓
- 内容适合拆成 4-8 页，每页一个观点 ✓
- 需要平台规格（1080×1440）✓
- 有截图、产品图或照片作为视觉证据 ✓

**输出：**
```md
输出模式：social-card
选择原因：小红书种草内容，需要视觉吸引力和传播性
预期卡片数量：6 页
平台规格：小红书 1080×1440
视觉导演：save_first（保存优先）
```

---

### 阶段 3：Execution Mode Router

**参考：** [03-execution-mode-router.md](03-execution-mode-router.md)

**判定执行路径：**

#### `direct_image_preview` - 直接生图预览
**适用场景：**
- 快速出样
- 验证 hook 和页面角色
- 不追求商用级别精度

---

#### `prompt_package` - 提示词包
**适用场景：**
- 需要场景感主视觉
- 需要插画感封面或情绪化背景
- 需要平台规格声明、内容压缩阶梯和分页脚本

**输出：** 每页提示词 + 渲染数据

---

#### `engineering_rendering` - 工程化渲染 ⭐ 推荐
**适用场景：**
- 批量生成
- 商用发布
- 截图必须精确
- 中文必须准确

**特点：** 单 HTML 多 frame 渲染，确保组图风格一致性

---

### 阶段 4：Content Analysis

**参考：** [04-content-analysis.md](04-content-analysis.md)

**提炼内容骨架：**
- 核心 hook（痛点/好奇/共鸣）
- 主线逻辑（问题 → 方案 → 证据 → 行动）
- 视觉证据（截图/产品图/对比图）
- 情绪基调（种草/避坑/教程/对比）

**输出：**
```md
## 内容骨架

核心 hook：时间总是不够用？试试这个神器
主线逻辑：痛点 → 功能亮点 → 使用场景 → 效果展示 → 行动
视觉证据：App 界面截图 5 张
情绪基调：种草 + 实用
```

---

### 阶段 4A：Content Compression Ladder ⭐ 必须

**触发条件：** 社交卡/长文拆页内容压缩

**目标：** 把长文压缩成适合社交平台的短内容

**压缩原则：**
- 一页一个核心点
- 删除冗余信息
- 保留关键证据
- 强化 hook 和行动号召

**输出：**
```md
## 内容压缩结果

原始内容：3000 字产品介绍
压缩后：6 页，每页 30-80 字
保留：核心功能、使用场景、视觉证据
删除：背景介绍、技术细节、冗余描述
```

---

### 阶段 4C：Visual Direction Routing ⭐ 默认启用

**参考：** `references/config/visual-direction-system.md`

**目标：** 视觉导演编排，决定视觉策略

**三种导演模式：**

#### `click_first` - 点击优先
**适用场景：**
- 标题党、悬念、好奇心驱动
- 需要快速抓眼球
- 封面图强视觉冲击

**特点：**
- 封面高视觉冲击
- 标题悬念感
- 前 3 页快速建立兴趣

---

#### `save_first` - 保存优先 ⭐ 推荐
**适用场景：**
- 干货、清单、教程、避坑指南
- 用户需要保存收藏
- 实用价值高

**特点：**
- 封面直接展示核心价值
- 页面信息密度高
- 结构化呈现
- 便于截图复用

---

#### `brand_first` - 品牌优先
**适用场景：**
- 品牌宣传
- 产品发布
- 官方账号

**特点：**
- 品牌视觉统一
- Logo/品牌色贯穿
- 专业感强

---

**本案例选择：** `save_first`（时间管理工具介绍，用户需要保存）

---

### 阶段 5：Page Script with Page Roles

**参考：** [05-carousel-script.md](05-carousel-script.md)

**页面角色编排：**
- **封面页** - hook + 主题
- **痛点页** - 建立共鸣
- **认知页** - 为什么需要这个方案
- **方法页** - 核心功能/方法
- **证据页** - 截图/数据/案例
- **操作页** - 如何使用
- **总结页** - 核心价值回顾
- **行动页** - 行动号召

**输出分页脚本：**

```md
## 6 页社交卡脚本

### 第 1 页：封面页
**页面角色：** 封面 + hook
**核心内容：** 时间总是不够用？试试这个神器
**视觉元素：** App 主界面截图 + 视觉吸引力装饰
**文字内容：**
  - 主标题：时间总是不够用？
  - 副标题：试试这个时间管理神器
  - hook 点：番茄钟 + 数据可视化 + 跨平台

---

### 第 2 页：痛点页
**页面角色：** 痛点 + 共鸣
**核心内容：** 3 个常见时间管理痛点
**视觉元素：** 痛点场景插图
**文字内容：**
  - 标题：这些痛点你中了几个？
  - 痛点 1：计划总是完不成
  - 痛点 2：不知道时间都去哪了
  - 痛点 3：多设备切换数据丢失

---

### 第 3 页：功能亮点 1
**页面角色：** 方法 + 证据
**核心内容：** 番茄钟功能
**视觉元素：** 番茄钟界面截图
**文字内容：**
  - 标题：番茄钟专注模式
  - 说明：25 分钟专注 + 5 分钟休息
  - 亮点：可自定义时长、白噪音、提醒

---

### 第 4 页：功能亮点 2
**页面角色：** 方法 + 证据
**核心内容：** 数据可视化
**视觉元素：** 数据统计界面截图
**文字内容：**
  - 标题：直观的数据可视化
  - 说明：每日/每周/每月专注时长统计
  - 亮点：成就徽章、专注排行

---

### 第 5 页：功能亮点 3
**页面角色：** 方法 + 证据
**核心内容：** 跨平台同步
**视觉元素：** 多设备同步效果图
**文字内容：**
  - 标题：无缝跨平台同步
  - 说明：iOS/Android/Web/Mac 数据实时同步
  - 亮点：一个账号，所有设备

---

### 第 6 页：总结 + 行动
**页面角色：** 行动号召
**核心内容：** 核心价值 + 下载方式
**视觉元素：** App icon + 下载二维码
**文字内容：**
  - 标题：开始高效时间管理
  - 核心价值：番茄钟 + 数据可视化 + 跨平台
  - 行动：扫码下载 / 应用商店搜索「XX 时间管理」
```

---

### 阶段 6：Prompt / Render Package

**参考：** [10-prompt-and-render-package.md](10-prompt-and-render-package.md)

#### 如果是 `engineering_rendering`（推荐）

**输出渲染数据包：**
```json
{
  "platform": "xiaohongshu",
  "visual_direction": "save_first",
  "style": {
    "background": "#FFFFFF",
    "primary_color": "#FF6B6B",
    "secondary_color": "#4ECDC4",
    "accent_color": "#FFE66D",
    "font_family": "PingFang SC"
  },
  "pages": [
    {
      "page_number": 1,
      "page_role": "cover",
      "title": "时间总是不够用？",
      "subtitle": "试试这个时间管理神器",
      "hook_points": ["番茄钟", "数据可视化", "跨平台"],
      "visual_asset": "app-main-screen.png",
      "layout": "hero-with-text"
    },
    {
      "page_number": 2,
      "page_role": "painpoint",
      "title": "这些痛点你中了几个？",
      "pain_points": [
        "计划总是完不成",
        "不知道时间都去哪了",
        "多设备切换数据丢失"
      ],
      "visual_hint": "painpoint-illustration",
      "layout": "list-with-icons"
    }
    // ... 其他页面
  ]
}
```

**使用模板：** `assets/render-engine/html-templates/social-card.html`

---

### 阶段 7：Batch Generation / Rendering

#### 执行路径 A：工程化渲染（推荐）
```
1. 准备渲染数据包（JSON）
2. 准备视觉资产（截图/产品图）
3. 调用单 HTML 多 frame 模板
4. 批量渲染 6 页
5. 输出 PNG 文件（1080×1440）
6. 检查风格一致性
```

**优势：**
- 风格完全统一
- 截图位置精确
- 中文文字准确
- 批量生成高效

---

### 阶段 8：Quality Gate

**质量检查清单：**

#### 平台规格（必须）
- [ ] 画幅 1080×1440 (3:4)
- [ ] 安全区内没有被裁切的关键内容
- [ ] 符合小红书/社交平台规范

#### 内容忠实度
- [ ] 每页内容与 Source Lock 一致
- [ ] 产品功能描述准确
- [ ] 截图与描述匹配
- [ ] 没有虚构功能

#### 视觉导演
- [ ] 封面符合导演模式（save_first）
- [ ] 页面角色编排合理
- [ ] hook 点突出
- [ ] 行动号召清晰

#### 风格一致性
- [ ] 6 页背景色一致
- [ ] 主色调统一
- [ ] 字体字号一致
- [ ] 版式规范统一

#### 传播性
- [ ] 封面吸引力强
- [ ] 每页可独立截图
- [ ] 核心信息密度适中
- [ ] 便于保存收藏

---

### 阶段 9：Retry / Production Upgrade

#### 不合格情况处理

**平台规格不符 →** 调整画幅到 1080×1440

**内容密度过高 →** 回到阶段 4A，进一步压缩内容

**视觉吸引力不足 →** 调整视觉导演模式或增强视觉元素

**风格不一致 →** 升级到 `engineering_rendering`

---

## 核心规则

### 硬规则
1. **No Source Lock, No Generation** - 没完成 Source Lock 不生成组图
2. **Platform Specs Before Social Cards** - 社交组图必须先声明平台规格（1080×1440）
3. **Content Fidelity First** - 产品功能描述必须准确
4. **Engineering Rendering For Production** - 批量/商用优先工程化渲染

### 推荐实践
- 必须声明平台规格（小红书/Instagram 等）
- 必须启用 Content Compression Ladder 压缩内容
- 必须启用 Visual Direction Routing 选择导演模式
- 页数建议 4-8 页
- 每页一个核心点
- 保持风格一致性
- 使用单 HTML 多 frame 渲染

---

## 视觉系统

### 画幅
- 标准：3:4 (1080×1440)
- 平台：小红书/Rednote/Instagram

### 导演模式
- **click_first** - 点击优先（悬念/标题党）
- **save_first** - 保存优先（干货/清单） ⭐ 推荐
- **brand_first** - 品牌优先（官方/品牌宣传）

### 页面角色
- 封面 - hook + 主题
- 痛点 - 建立共鸣
- 认知 - 为什么需要
- 方法 - 核心功能
- 证据 - 截图/数据
- 操作 - 如何使用
- 总结 - 核心价值
- 行动 - 行动号召

---

## 参考资源

### 模板族
- [template-families/social-card/](../template-families/social-card/)

### 配置文件
- [config/visual-direction-system.md](../config/visual-direction-system.md) ⭐
- [config/risk-action-blacklist.md](../config/risk-action-blacklist.md)
- [config/asset-source-policy.md](../config/asset-source-policy.md)

### 渲染引擎
- `assets/render-engine/html-templates/social-card.html`
- `assets/render-engine/css/social-card.css`

---

**版本：** 1.0.0  
**最后更新：** 2026-06-16  
**维护：** Content Visual Forge
