---
name: awesun-remote-control
description: 向日葵远程控制(awesun-remote-control) 提供 22 个工具。使用场景包括：控制命令、控制连接、控制断开。关键词：远程控制，设备管理，桌面控制，远程CMD，远程电源管理。
version: 1.0
---

# awesun-remote-control

向日葵远程控制(awesun-remote-control) 提供 22 个远程设备管理与操作工具。包括：设备管理，远程连接，远程桌面控制，远程命令执行，远程电源管理等功能。适用于需要通过编辑器对远程设备进行全面控制的场景。

## Available Tools (22)

### Device

- `device_add` - 将新设备添加到设备列表中，可设置设备名称和描述便于管理。添加成功后可通过 device_search 查询该设备。
    - **Required parameters**:
      - `name` (string): 设备的名称
    - **Optional parameters**:
      - `desc` (string): 设备的描述信息
- `device_info` - 查询指定设备的完整详细信息，包括硬件配置（CPU、内存、硬盘、显卡）、网络信息（IP地址、MAC地址）、系统版本、在线状态、支持的插件等。必须先通过 device_search 获取设备ID。
    - **Required parameters**:
      - `remote_id` (integer): 设备ID
- `device_remove` - 从设备列表中删除指定的设备，仅移除列表记录不会影响被控端软件，删除后无法恢复。删除前建议确认设备已不再需要使用。
    - **Required parameters**:
      - `remote_id` (integer): 设备ID
- `device_search` - 根据关键词模糊搜索设备列表中的设备，支持按设备名称检索，返回匹配的设备基本信息列表。常用于查找特定设备以进行后续远控操作。
    - **Required parameters**:
      - `limit` (integer): 查询结果数量限制，最大值为100
    - **Optional parameters**:
      - `keyword` (string): 查询关键字，支持模糊检索
- `device_shutdown` - 向在线的远程设备发送关机指令，设备需处于在线状态且被控端支持关机功能。指令下发后设备将在1-2分钟内完成关机并离线。
    - **Required parameters**:
      - `remote_id` (integer): 设备ID
- `device_update` - 修改指定设备的名称和描述信息，用于更新设备列表中的显示名称和备注，便于设备管理和识别。
    - **Required parameters**:
      - `remote_id` (integer): 设备ID
    - **Optional parameters**:
      - `desc` (string): 设备的描述信息
      - `name` (string): 设备的名称
- `device_wakeup` - 向绑定了开机硬件的设备发送开机指令，需要设备端配置开机棒或主板支持WOL功能。指令下发后设备将在1-2分钟内完成开机并上线。
    - **Required parameters**:
      - `remote_id` (integer): 设备ID

### Control

- `control_connect` - 发起与指定设备的远控会话连接，支持远程文件(file)、远程桌面(desktop)、远程CMD(cmd2)、远程SSH(ssh)、桌面观看(desktop_view)、远程摄像头(newcamera)、端口转发(forward)。连接成功后返回会话ID，用于后续的桌面操作、截图、命令执行等。
    - **Required parameters**:
      - `type` (string): 远控类型（远程文件=file|远程桌面=desktop|远程CMD=cmd2(适用于Windows)|远程SSH=ssh(适用于Linux/Mac)|桌面观看=desktop_view|摄像头=newcamera|端口转发=forward）
    - **Optional parameters**:
      - `remote_id` (integer): 被控设备ID（通过设备列表已存在的设备发起远控）
- `control_disconnect` - 终止指定的活跃远控会话，立即断开与该会话的连接。断开后如需再次操作需要重新调用 control_connect 建立连接。建议在不使用会话时及时断开以释放资源。
    - **Required parameters**:
      - `session_id` (string): 远控会话ID
- `control_portforward` - 在已建立的端口转发远程会话中配置端口转发规则（覆盖），需先建立有效的端口转发远程会话，用于实现本地与远程主机端口的双向数据转发。
    - **Required parameters**:
      - `session_id` (string): 远控会话ID（仅支持forward类型的远程会话）
      - `target_addresses` (array): 内网目标主机的IP或主机名:协议端口（仅支持TCP协议，支持同时配置多个，如：['127.0.0.1:22'
- `control_screenshot` - 对指定的远程桌面会话(desktop/desktop_view)进行截图，返回Base64编码的图片数据及尺寸信息。截图可用于获取远程设备的当前画面状态，辅助判断操作结果。
    - **Required parameters**:
      - `session_id` (string): 远控会话ID（仅支持desktop/desktop_view类型的远程会话）
- `control_sessions` - 查询所有当前活跃的远控会话，包括会话ID/会话类型和状态。获取的会话ID可用于截图、执行命令、桌面操作、断开连接等后续操作。
    - **Optional parameters**:
      - `type` (string): 远控类型，不传则返回所有远控会话（远程文件=file|远程桌面=desktop|远程CMD=cmd2|远程SSH=ssh|桌面观看=desktop_view|摄像头=newcamera|端口转发=forward）
- `control_command` - 在已建立的CMD远程会话中执行命令，目前支持Windows的CMD。返回命令的退出码、标准输出和错误输出。
    - **Required parameters**:
      - `command` (string): 要执行的命令
      - `session_id` (string): 远控会话ID（仅支持cmd2类型的远程会话）
    - **Optional parameters**:
      - `args` (array): 命令参数

### Desktop

- `desktop_click_mouse` - 在远程桌面会话中模拟鼠标点击操作，支持左键、右键、中键点击及双击。坐标需使用归一化值(0.0-1.0)，通过 x_pixel/屏幕宽度 计算。适用于按钮点击、菜单选择等场景。
    - **Required parameters**:
      - `button` (string): 点击鼠标按钮类型，可选值有：left
      - `clicks` (integer): 点击次数，传2则为双击
      - `coordinates` (array): 需要点击的坐标[x
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
- `desktop_drag_mouse` - 在远程桌面中模拟鼠标拖拽操作，支持按住指定按键(left/right/middle)沿路径移动。可用于文件拖拽、窗口调整大小、选择文本区域等。路径坐标需归一化(0.0-1.0)。
    - **Required parameters**:
      - `button` (string): 拖拽鼠标按钮类型，可选值有：left
      - `paths` (array): 滚动路径，每个坐标一组，格式['x
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
    - **Optional parameters**:
      - `hold_keys` (array): 拖拽鼠标时按下的键，可选值有：shift
- `desktop_move_mouse` - 将鼠标光标移动到远程桌面的指定坐标位置，坐标需归一化(0.0-1.0)。常用于拖拽操作前的定位、悬停触发菜单、或配合截图确定点击位置。仅移动不触发点击。
    - **Required parameters**:
      - `coordinates` (array): 目标坐标[x
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
- `desktop_paste_text` - 在远程桌面中通过系统剪贴板粘贴长文本内容，比逐字符输入更高效。适用于输入大段文本、代码、命令等场景。使用前需确保输入框已获取焦点，且被控端支持剪贴板同步。
    - **Required parameters**:
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
      - `text` (string): 需要粘贴的文本字符串
- `desktop_press_keys` - 在远程桌面中精确控制按键的按下或释放操作，适合需要精细控制按键状态的场景。支持单独按下(down)、单独释放(up)，或不指定时自动按下后释放。可用于长按、连击等复杂操作。
    - **Required parameters**:
      - `keys` (array): 按键序列，如control
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
    - **Optional parameters**:
      - `press` (string): 按键操作，可选值有：up/down (如果不填则默认为先按下后释放，如果传入down，则一定要再调用一次up)
- `desktop_scroll_mouse` - 在远程桌面的指定位置模拟鼠标滚轮滚动，支持向上(up)或向下(down)滚动指定次数。用于滚动网页、文档、列表等内容查看。坐标需归一化(0.0-1.0)。
    - **Required parameters**:
      - `coordinates` (array): 坐标[x
      - `direction` (string): 滚动方向，可选值有：up
      - `scroll_count` (integer): 滚动次数
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
- `desktop_typing_keys` - 在远程桌面中执行组合快捷键操作，如复制(Ctrl+C)、粘贴(Ctrl+V)、保存(Ctrl+S)等。按顺序按下所有按键，延迟后再按相反顺序释放。适合需要同时按住多个键的场景。
    - **Required parameters**:
      - `keys` (array): 按顺序键入的键名称数组，如control
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
    - **Optional parameters**:
      - `delay` (integer): 按下和释放按键之间的延迟（以毫秒为单位）
- `desktop_typing_text` - 在远程桌面中逐字符模拟键盘输入文本，适合输入短文本内容。输入前需确保输入框已获取焦点。可设置字符间延迟(毫秒)控制输入速度。
    - **Required parameters**:
      - `session_id` (string): 远控会话ID（仅支持desktop类型的远程会话）
      - `text` (string): 需要输入的文本字符串
    - **Optional parameters**:
      - `delay` (integer): 字符输入间隔，单位毫秒
- `desktop_waiting` - 在远控操作序列中插入暂停等待，用于在关键操作后等待系统响应或页面加载完成。指定持续时间(毫秒)后自动继续执行后续工具。建议在网络延迟或UI渲染场景中使用。
    - **Required parameters**:
      - `duration` (integer): 暂停时间单位：毫秒（UI 渲染等待建议：≤500ms，避免过长等待）

## Instructions

### Standard Call Flow

1. **Identify the tool** - Choose the appropriate tool from the list above
2. **Get tool parameters** (optional) - If unsure about parameter format:

   ```bash
   cd ~/.claude/skills/awesun-remote-control
   python executor.py --describe <tool_name>
   ```

3. **Execute the tool call**:

   ```bash
   cd ~/.claude/skills/awesun-remote-control
   python executor.py --call '{"tool": "<tool_name>", "arguments": {...}}'
   ```

If `python` command not found, try `python3` instead.

### Error Handling

If execution fails:

- Check tool name is correct
- Use `--describe` to view required parameters
- Ensure MCP server is accessible

## Examples

```bash
# List all tools
python executor.py --list

# Get tool details
python executor.py --describe <tool_name>

# Execute a tool
python executor.py --call '{"tool": "example", "arguments": {}}'
```
