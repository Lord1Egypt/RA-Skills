# deepaistudy-errors Skill

深智智错题本 Skill。拍照上传错题，AI 自动分析并生成变式题。支持标记掌握状态。

**与 `deepaistudy-prep` 共用同一套认证配置**，无需重复登录。

## 工作原理

```
错题图片 → [AI 分析] → 错题记录
```

## 前置要求

1. **已配置认证**（与 deepaistudy-prep 共用）：
   ```bash
   deepaistudy-errors config set server   https://www.deepaistudy.com
   deepaistudy-errors config set username your_email@domain.com
   deepaistudy-errors config set password your_password
   ```
2. **AI 分析约需 1-3 分钟**：请耐心等待

## 使用方式

### 添加错题（推荐）

拍照错题，上传后自动 AI 分析：

```bash
deepaistudy-errors add /path/to/error1.jpg /path/to/error2.jpg \
  --subject 数学 \
  --title "分数运算易错题"
```

会自动轮询分析状态，完成后显示结果。

### 列出错题

```bash
# 全部
deepaistudy-errors list

# 按学科筛选
deepaistudy-errors list --subject 数学

# 搜索关键词
deepaistudy-errors list --search "分数"
```

### 轮询分析状态

```bash
deepaistudy-errors status <task_id> --interval 5
```

### 标记掌握状态

```bash
deepaistudy-errors master 123    # 标记为已掌握
deepaistudy-errors unmaster 123  # 取消已掌握
```

### 生成变式题

```bash
# 默认3道中等难度
deepaistudy-errors variation 123

# 指定数量和难度
deepaistudy-errors variation 123 --count 5 --difficulty hard
```

### 删除错题

```bash
deepaistudy-errors delete 123
```

## 配置

```bash
# 与 deepaistudy-prep 共用，无需单独配置
deepaistudy-errors config list
```

## 返回内容

添加成功后返回：

- `id`：错题记录 ID
- `subject`：学科
- `title`：标题
- `content`：错题内容（学生答案 / 正确答案 / 解析）
- `mastery_status`：掌握状态（已掌握 / 未掌握）
- `exercise_images`：原始错题图片

## 状态说明

| 状态 | 说明 |
|------|------|
| 已掌握 | 错题已复习完成 |
| 未掌握 | 还需要复习 |

## 常用命令汇总

| 命令 | 说明 |
|------|------|
| `add <images> --subject X` | 添加错题 + AI 分析 |
| `list --subject X` | 错题列表 |
| `status <task_id>` | 轮询分析状态 |
| `master <note_id>` | 标记已掌握 |
| `unmaster <note_id>` | 取消已掌握 |
| `variation <note_id> -n 3` | 生成变式题 |
| `delete <note_id>` | 删除错题 |
| `config set key value` | 设置配置 |

## 注意事项

- 图片会压缩到最大 2048px
- 支持一次识别多道错题（自动从整页作业/试卷中提取）
- 标记已掌握后，错题不会出现在"待复习"列表
- 变式题用于举一反三，巩固同类题型
