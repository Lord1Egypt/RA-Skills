# AI编程工具工具定义参考库

## 工具分类总览

### 分类体系

```yaml
五大类别:
  1. 文件操作类
     - 读取、写入、编辑、删除

  2. 搜索查询类
     - 内容搜索、文件搜索、语义搜索

  3. 执行操作类
     - Shell命令、进程管理

  4. 浏览器操作类
     - 导航、交互、截图

  5. 部署运维类
     - 部署、监控、日志
```

## 文件操作类工具

### 1. Read - 读取文件

#### Cursor定义
```yaml
名称: read_file
描述: 读取文件内容
参数:
  - name: path
    type: string
    required: true
    description: 文件的绝对路径
  - name: start_line
    type: number
    required: false
    description: 起始行号
  - name: end_line
    type: number
    required: false
    description: 结束行号
特点:
  - 范围读取支持
  - 长文件自动截断
  - 编码自动处理
```

#### Claude Code定义
```yaml
名称: Read
描述: 读取文件内容
参数:
  - name: file_path
    type: string
    required: true
    description: 文件路径
返回:
  - 文件内容
  - 行号范围
  - 截断信息
特点:
  - 上下文感知
  - 智能截断
  - 编码检测
```

### 2. Write - 写入文件

#### Cursor定义
```yaml
名称: create_file
描述: 创建新文件
参数:
  - name: path
    type: string
    required: true
    description: 文件绝对路径
    约束: 文件必须不存在
  - name: content
    type: string
    required: true
    description: 文件内容
特点:
  - 不覆盖现有文件
  - 自动创建目录
  - 内容精确写入
```

### 3. Edit - 编辑文件

#### Cursor定义
```yaml
名称: search_replace
描述: 精确字符串替换
参数:
  - name: path
    type: string
    required: true
    description: 文件路径
  - name: old_str
    type: string
    required: true
    description: 原字符串
    约束: 必须唯一匹配
  - name: new_str
    type: string
    required: true
    description: 新字符串
规则:
  1. old_str必须精确匹配
  2. 包括所有空白字符
  3. 不能包含部分行
  4. 建议使用注释标记未修改部分
```

## 搜索查询类工具

### 1. Grep - 正则搜索

#### Cursor定义
```yaml
名称: grep_code
描述: 基于正则的文件内容搜索
参数:
  - name: path
    type: string
    required: true
    description: 搜索路径
  - name: regex
    type: string
    required: true
    description: 正则表达式
  - name: file_extension
    type: string
    required: false
    description: 文件扩展名过滤
返回:
  - 文件路径
  - 匹配行号
  - 匹配内容
  - 上下文
限制:
  - 默认最多50条结果
```

### 2. Glob - 文件名搜索

#### Cursor定义
```yaml
名称: search_file
描述: 基于模糊匹配的文件路径搜索
参数:
  - name: path
    type: string
    required: true
    description: 搜索目录
  - name: pattern
    type: string
    required: true
    description: glob模式
    示例: "**/*.js", "src/**/*.ts"
特点:
  - 支持通配符
  - 递归搜索
  - 模糊匹配
限制:
  - 默认最多10条结果
```

### 3. Semantic Search - 语义搜索

#### Cursor定义
```yaml
名称: semantic_search
描述: 语义级代码搜索
参数:
  - name: query
    type: string
    required: true
    description: 语义查询
    示例: "用户认证逻辑", "权限检查函数"
特点:
  - 理解代码语义
  - 不依赖关键词
  - 返回相关代码片段
优势:
  - 发现隐含关联
  - 理解业务逻辑
  - 跨语言支持
```

## 执行操作类工具

### 1. Bash - Shell执行

#### Cursor定义
```yaml
名称: run_in_terminal
描述: 执行Shell命令
参数:
  - name: command
    type: string
    required: true
    description: Shell命令
  - name: cwd
    type: string
    required: false
    description: 工作目录
  - name: timeout
    type: number
    required: false
    description: 超时(秒)
  - name: is_background
    type: boolean
    required: false
    description: 后台执行
返回:
  - 标准输出
  - 标准错误
  - 退出码
注意:
  - 禁止用于文件操作
  - 禁止用于搜索操作
```

## 浏览器操作类工具

### Devin浏览器工具集

```yaml
基础导航:
  1. navigate_browser
     参数:
       - name: url
         required: true
       - name: tab_idx
         required: false
         默认: 0

  2. view_browser
     参数:
       - name: reload_window
         type: boolean
       - name: scroll_direction
         type: string

交互操作:
  1. click_browser
     参数:
       - name: devinid
         type: string
       - name: coordinates
         type: string

  2. type_browser
     参数:
       - name: devinid
         type: string
       - name: press_enter
         type: boolean

元素定位:
  定位方式优先级:
    1. devinid (推荐)
       - 自动注入
       - 最可靠

    2. coordinates (备选)
       - 像素坐标
       - 最后手段
```

## 工具能力对比

### 文件操作能力对比

| 工具 | Read | Write | Edit | Delete | 特点 |
|------|------|-------|------|--------|------|
| Cursor | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 精确替换 |
| Claude | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 上下文感知 |
| Devin | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 批量编辑 |
| Windsurf | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 标准操作 |

### 搜索能力对比

| 工具 | Grep | Glob | Semantic | 特点 |
|------|------|------|----------|------|
| Cursor | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 语义优先 |
| Claude | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 精确匹配 |
| Devin | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 正则强大 |
| Windsurf | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 标准搜索 |

### 执行能力对比

| 工具 | Bash | 并行执行 | 后台进程 | 特点 |
|------|------|---------|---------|------|
| Cursor | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 基础支持 |
| Claude | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 完善支持 |
| Devin | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Shell管理 |
| Windsurf | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 标准支持 |

### 浏览器能力对比

| 工具 | 导航 | 交互 | 截图 | 自动化 |
|------|------|------|------|--------|
| Cursor | ⭐⭐ | ⭐⭐ | ⭐ | 基础 |
| Claude | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | 中等 |
| Devin | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 完善 |
| Windsurf | ⭐⭐ | ⭐⭐ | ⭐ | 基础 |

## 工具定义JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "工具唯一名称"
    },
    "description": {
      "type": "string",
      "description": "工具功能描述"
    },
    "parameters": {
      "type": "object",
      "properties": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "type": {"type": "string"},
          "required": {"type": "boolean"},
          "description": {"type": "string"},
          "default": {}
        }
      }
    },
    "returns": {
      "type": "object",
      "properties": {
        "type": {"type": "string"},
        "description": {"type": "string"}
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {"type": "string"},
          "handling": {"type": "string"}
        }
      }
    }
  }
}
```
