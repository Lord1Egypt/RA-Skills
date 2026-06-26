# 交互规则参考

## 目录

- [模型选择示例](#模型选择示例)
- [生成类型选择示例](#生成类型选择示例)
- [级联参数选择框示例](#级联参数选择框示例)
- [选择框规则汇总](#选择框规则汇总)
- [提示词润色交互](#提示词润色交互)
- [画幅自然语言映射](#画幅自然语言映射)
- [展示约束](#展示约束)

---

## 模型选择示例

### 情况 B：2-4 个模型

```text
AskUserQuestion with questions array:
  [
    {
      header: "选择模型",
      question: "选择视频模型",
      multiSelect: false,
      options: [
        // 从 /video/config 返回的 data 数组动态生成
        // 每个 option 的 label 取 model_name，description 取 model_code
        { label: data[0].model_name, description: data[0].model_code },
        { label: data[1].model_name, description: data[1].model_code },
        ...
      ]
    },
  ]
```

### 情况 C：5 个及以上模型

`AskUserQuestion` 最多 4 个选项，无法容纳。改为文本编号列表 + 自由输入：

```text
当前可用的视频模型如下，请回复编号或名称选择：

1. 可灵 视频模型 — 支持文生视频与图生视频
2. Vidu 视频模型 — 速度快，长提示词
3. PixVerse — 时长灵活（1-15s）
4. Veo 视频模型 — 高画质，支持 1080p
5. Wan 视频模型 — 风格化生成
6. ...

直接回复编号（如 "1"）或模型名（如 "可灵"）即可。
```

用户回复后，模糊匹配模型名称或精确匹配编号。匹配不到则提示重新选择。

---

## 生成类型选择示例

生成类型不是互斥的 — 必须遍历所有方案，把所有符合条件的类型都列出来。只命中 1 种时才静默应用，否则必须弹选择框。

```text
AskUserQuestion with questions array:
  [
    {
      header: "生成类型",
      question: "选择生成类型",
      multiSelect: false,
      options: [
        { label: "文生视频", description: "输入提示词，AI 生成视频" },
        { label: "图生视频", description: "提供一张图片作为起始帧" },
        { label: "首尾帧", description: "提供首帧（必须）和尾帧（可选），AI 生成过渡" }
        // 如果方案 last_frame = 0，则该选项改为：
        // { label: "首帧", description: "提供首帧图片，AI 生成视频" }
        // 根据实际支持的类型动态生成，必须列出所有命中的类型
      ]
    }
  ]
```

---

## 级联参数选择框示例

把同一模型下所有需要用户选择的选项数组尽量合并到一个 `AskUserQuestion` 调用中。**有合理推荐理由时**（用户暗示偏好、选项明显更通用、能降低成本），把推荐项放第一位并加 `(推荐)`。没有明确倾向时不标推荐。

```text
AskUserQuestion with questions array:
  [
    {
      header: "画面比例",
      question: "选择画面比例",
      multiSelect: false,
      options: [
        { label: "16:9", description: "横屏（适合宽屏/电脑）" },
        { label: "9:16", description: "竖屏（适合手机/短视频）" },
        { label: "1:1", description: "方形（适合朋友圈/社交平台）" }
      ]
    },
    {
      header: "视频时长",
      question: "选择视频时长",
      multiSelect: false,
      options: [
        { label: "5秒", description: "短片段，生成快、省积分" },
        { label: "10秒", description: "标准时长" },
        { label: "15秒", description: "长片段，适合完整叙事" }
      ]
      // 用户可通过自带的 "Other" 选项输入任意秒数，如 "3秒"、"8秒"
    }
  ]
```

---

## 选择框规则汇总

- 选项数组只有 1 个值时，静默应用，不需要用户选
- 选项数组有 2-4 个值时，直接放进 `AskUserQuestion` 选择框
- 选项数组超过 4 个值时（如 `duration: ["1","2",...,"15"]`），**从中选取 3-4 个最常用的值作为选项**，用户可通过自带的 "Other" 输入其他值。不要降级为纯文本输入
- 多个选项数组尽量合并到同一个 `AskUserQuestion`（最多 4 个 question），一次问完
- 如果需要用户选择的维度超过 4 个，分多轮 `AskUserQuestion` 连续收集，每轮最多 4 个问题。优先把最影响结果的维度（画面比例、时长）放在第一轮
- 提示词在第 5 步收集：足够具体时直接使用，薄弱时通过 `AskUserQuestion` 展示原始版/润色版选项
- **有限选项必须用选择框，绝对不要用纯文本列表让用户手动输入**

---

## 提示词润色交互

如果提示词明显太薄（例如"来个视频"、"海边日出"、"一个女孩"这种只有主题没有细节的），不要直接追问"能不能告诉我更多"，而是 **主动润色后直接弹出选择框**：

1. 根据用户给出的关键词 + 已选模型的能力，自动扩写出一段完整的提示词（补充场景细节、氛围、镜头语言等）
2. **直接弹出 `AskUserQuestion`，前面不要输出任何文字**（不要写"您的提示词比较简短"、"我帮您润色了一版"等）：

```text
AskUserQuestion:
  header: "提示词"
  question: "选择提示词版本"
  multiSelect: false
  options:
    - label: "使用原始版"
      description: "海边日出"
    - label: "使用润色版"
      description: "海边黄昏，金色阳光洒在沙滩上，一个女孩赤脚走在浪花边缘，电影感镜头缓慢推进，暖色调"
```

规则：
- 润色时结合上下文：如果用户提供了参考图，润色内容要和图片内容呼应
- 润色结果保持在 200 字符以内，不要过度堆砌
- 用户可通过自带的 "Other" 选项输入自定义提示词
- 如果用户的提示词本身就足够具体（有主体 + 场景 + 至少一个修饰词），跳过润色，直接进入下一步

---

## 画幅自然语言映射

- "竖屏" / "portrait" / "vertical" / "手机" → `9:16`
- "横屏" / "landscape" / "horizontal" → `16:9`
- "方形" / "square" / "朋友圈" → `1:1`

---

## 展示约束

### 不要向用户展示的内容

不要暴露或询问：供应商名称、`mode`、`model_name`、子模型代码、内部路由字段。这些由用户选择的参数组合决定，后端自动匹配方案。

**以下内部标识符不要出现在任何面向用户的文本中**（包括摘要、确认框、状态报告、错误提示）：
- `model_code` — 用模型名称代替
- `internalTaskId`、`capability` — 纯内部字段
- `prompt` 这个词本身 — 对用户统一称为"提示词"

### 需要展示给用户的标识符

- `taskId`（`task_xxx`）— 任务提交成功后展示
- `requestId`（`req_xxx`）— 任务提交成功后展示
