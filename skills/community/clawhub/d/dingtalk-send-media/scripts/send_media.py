#!/usr/bin/env python3
"""
钉钉媒体文件发送脚本
支持发送图片、文件到钉钉用户或群聊

特性：
- 自动从 OPENCLAW_AGENT_ID 检测钉钉账号
- 跨平台支持（Windows/Linux/macOS）
- 零第三方依赖（仅使用 Python 标准库）
- 支持多种媒体类型（image/voice/video/file）
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import urllib.error
import mimetypes
import uuid
from pathlib import Path


def has_direct_env_credentials():
    """是否直接提供了钉钉凭证环境变量"""
    return bool(
        os.environ.get('DINGTALK_CLIENTID', '') and
        os.environ.get('DINGTALK_CLIENTSECRET', '')
    )


def get_home_dir():
    """获取用户主目录"""
    if os.name == 'nt':
        return os.environ.get('USERPROFILE', '')
    return os.path.expanduser('~')


def get_config_path():
    """获取 OpenClaw 配置文件路径"""
    # 优先使用环境变量
    env_config = os.environ.get('OPENCLAW_CONFIG', '')
    if env_config and os.path.exists(env_config):
        return env_config
    
    # 默认路径
    default_path = os.path.join(get_home_dir(), '.openclaw', 'openclaw.json')
    if os.path.exists(default_path):
        return default_path
    
    return None


def load_openclaw_config():
    """加载 OpenClaw 配置文件"""
    config_path = get_config_path()
    if not config_path:
        if has_direct_env_credentials():
            return {}
        raise FileNotFoundError("未找到 OpenClaw 配置文件 openclaw.json，且未设置 DINGTALK_CLIENTID / DINGTALK_CLIENTSECRET")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def detect_account_from_agent_id(openclaw_config, agent_id=None, account_id=None, channel_account=None):
    """
    从多个来源自动检测钉钉账号
    
    优先级：
    1. 显式传入的 account_id（最高优先级）
    2. OPENCLAW_ACCOUNT_ID 环境变量
    3. channel_account 参数（从当前会话上下文传入）
    4. OPENCLAW_AGENT_ID + bindings 映射
    5. 从 agent ID 后缀提取（如 dingtalk-office → office）
    6. openclaw.json 中的 defaultAccount 配置
    7. 自动检测 dingtalk-connector 配置（新增）
    8. 自动检测 dingtalk.accounts 配置
    9. 默认返回 'prd_bot'

    Args:
        openclaw_config: OpenClaw 配置对象
        agent_id: Agent ID（可选）
        account_id: 显式指定的账号 ID（可选）
        channel_account: 从会话上下文传入的账号（可选）

    Returns:
        tuple: (account_id, source) - 账号 ID 和来源说明
    """
    # 优先级 1: 显式传入
    if account_id:
        return account_id, 'explicit_parameter'

    # 优先级 2: 环境变量 OPENCLAW_ACCOUNT_ID（直接指定账号）
    env_account = os.environ.get('OPENCLAW_ACCOUNT_ID', '')
    if env_account:
        return env_account, 'OPENCLAW_ACCOUNT_ID'

    # 优先级 2.5: 直接环境变量凭证
    if has_direct_env_credentials():
        return '__env__', 'direct_env_credentials'

    # 优先级 3: 从会话上下文传入的账号（direct runtime 模式）
    if channel_account:
        return channel_account, 'channel_context'

    # 优先级 4: OPENCLAW_AGENT_ID + bindings 映射
    if not agent_id:
        agent_id = os.environ.get('OPENCLAW_AGENT_ID', '')

    if agent_id:
        bindings = openclaw_config.get('bindings', [])

        # 查找匹配 binding
        for binding in bindings:
            if binding.get('agentId') == agent_id:
                match = binding.get('match', {})
                if match.get('channel') in ('dingtalk', 'dingtalk-connector'):
                    account_id = match.get('accountId')
                    if account_id:
                        return account_id, f'binding:{agent_id}→{account_id}'

        # Fallback: 从 agent ID 提取后缀
        if agent_id.startswith('dingtalk-'):
            return agent_id.replace('dingtalk-', ''), f'agent_suffix:{agent_id}'

    # 优先级 5: openclaw.json 中的 defaultAccount 配置
    channels = openclaw_config.get('channels', {})
    dingtalk = channels.get('dingtalk', {})
    default_account = dingtalk.get('defaultAccount')
    if default_account:
        return default_account, 'defaultAccount_config'

    connector = channels.get('dingtalk-connector', {})
    connector_default_account = connector.get('defaultAccount')
    if connector_default_account:
        return connector_default_account, 'dingtalk_connector.defaultAccount'

    # 优先级 6: 自动检测 dingtalk-connector.accounts 配置
    connector_accounts = connector.get('accounts', {})
    if connector_accounts:
        connector_account_keys = list(connector_accounts.keys())
        if len(connector_account_keys) == 1:
            return connector_account_keys[0], 'single_connector_account_auto'
        raise ValueError(
            f"检测到多个 dingtalk-connector 账号配置：{', '.join(connector_account_keys)}，"
            f"请通过以下方式之一指定使用哪个账号：\n"
            f"  1. 设置 OPENCLAW_ACCOUNT_ID 环境变量\n"
            f"  2. 配置 bindings 映射\n"
            f"  3. 在命令行显式指定账号参数"
        )

    # 优先级 7: 自动检测 dingtalk-connector 顶层配置
    dingtalk_connector = channels.get('dingtalk-connector', {})
    if dingtalk_connector.get('clientId'):
        # 使用 connector 配置，账号 ID 固定为 'connector'
        return 'connector', 'dingtalk-connector'

    # 优先级 8: 自动检测 dingtalk.accounts 配置
    accounts = dingtalk.get('accounts', {})
    if accounts:
        account_keys = list(accounts.keys())
        if len(account_keys) == 1:
            # 只有一个账号，自动使用
            return account_keys[0], 'single_account_auto'
        elif len(account_keys) > 1:
            # 多个账号但没有指定使用哪个，报错
            raise ValueError(
                f"检测到多个钉钉账号配置：{', '.join(account_keys)}，"
                f"请通过以下方式之一指定使用哪个账号：\n"
                f"  1. 设置 OPENCLAW_ACCOUNT_ID 环境变量\n"
                f"  2. 配置 bindings 映射\n"
                f"  3. 在命令行显式指定账号参数"
            )

    if has_direct_env_credentials():
        return '__env__', 'direct_env_credentials'

    # 没有任何钉钉账号配置，报错
    raise ValueError(
        "未在 openclaw.json 中找到钉钉账号配置。\n"
        "请在 channels.dingtalk.accounts 或 channels.dingtalk-connector 中配置。"
    )


def get_dingtalk_config(openclaw_config, account_id='prd_bot'):
    """
    从 OpenClaw 配置中提取钉钉配置
    
    优先级（环境变量优先级最高）：
    1. 直接读取 DINGTALK_* 环境变量（最高优先级，显式覆盖）
    2. openclaw.json 中的 ${VAR} 占位符
    3. openclaw.json 中的显式配置
    4. 报错
    """
    channels = openclaw_config.get('channels', {})

    # 处理环境变量占位符的辅助函数
    def resolve_env(value):
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            return os.environ.get(env_var, value)
        return value

    # 优先级 1：直接读取环境变量（最高优先级，显式覆盖）
    env_client_id = os.environ.get('DINGTALK_CLIENTID', '')
    env_client_secret = os.environ.get('DINGTALK_CLIENTSECRET', '')
    
    if env_client_id and env_client_secret:
        # 从环境变量获取时，robotCode 默认使用 clientId
        env_robot_code = os.environ.get('DINGTALK_ROBOTCODE', env_client_id)
        return {
            'clientId': env_client_id,
            'clientSecret': env_client_secret,
            'robotCode': env_robot_code,
            'corpId': os.environ.get('DINGTALK_CORPID', ''),
            'agentId': os.environ.get('DINGTALK_AGENTID', ''),
        }

    # 优先级 2 & 3：从配置文件获取

    # 纯环境变量模式
    if account_id == '__env__':
        if not env_client_id or not env_client_secret:
            raise ValueError("环境变量模式下缺少 DINGTALK_CLIENTID 或 DINGTALK_CLIENTSECRET")
        env_robot_code = os.environ.get('DINGTALK_ROBOTCODE', env_client_id)
        return {
            'clientId': env_client_id,
            'clientSecret': env_client_secret,
            'robotCode': env_robot_code,
            'corpId': os.environ.get('DINGTALK_CORPID', ''),
            'agentId': os.environ.get('DINGTALK_AGENTID', ''),
        }

    # 支持 dingtalk-connector 配置
    if account_id == 'connector':
        dingtalk_connector = channels.get('dingtalk-connector', {})

        client_id = resolve_env(dingtalk_connector.get('clientId', ''))
        return {
            'clientId': client_id,
            'clientSecret': resolve_env(dingtalk_connector.get('clientSecret', '')),
            'robotCode': resolve_env(dingtalk_connector.get('robotCode', client_id)),
            'corpId': '',
            'agentId': '',
        }

    # dingtalk-connector.accounts 配置
    connector_accounts = channels.get('dingtalk-connector', {}).get('accounts', {})
    if account_id in connector_accounts:
        account = connector_accounts[account_id]
        return {
            'clientId': resolve_env(account.get('clientId', '')),
            'clientSecret': resolve_env(account.get('clientSecret', '')),
            'robotCode': resolve_env(account.get('robotCode', account.get('clientId', ''))),
            'corpId': resolve_env(account.get('corpId', '')),
            'agentId': resolve_env(account.get('agentId', '')),
        }

    # 传统 dingtalk.accounts 配置
    dingtalk = channels.get('dingtalk', {})
    accounts = dingtalk.get('accounts', {})

    if account_id in accounts:
        account = accounts[account_id]
        return {
            'clientId': resolve_env(account.get('clientId', '')),
            'clientSecret': resolve_env(account.get('clientSecret', '')),
            'robotCode': resolve_env(account.get('robotCode', account.get('clientId', ''))),
            'corpId': resolve_env(account.get('corpId', '')),
            'agentId': resolve_env(account.get('agentId', '')),
        }

    # 没有任何配置，报错
    raise ValueError(
        f"未找到钉钉账号配置：{account_id}\n"
        "请设置环境变量或在 openclaw.json 中配置：\n"
        "  - DINGTALK_CLIENTID (环境变量，优先级最高)\n"
        "  - DINGTALK_CLIENTSECRET (环境变量，优先级最高)\n"
        "  - 或在 openclaw.json 的 channels.dingtalk.accounts / channels.dingtalk-connector 中配置"
    )


def get_access_token(client_id, client_secret):
    """获取钉钉 access token"""
    url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    data = json.dumps({
        'appKey': client_id,
        'appSecret': client_secret
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('accessToken')
    except urllib.error.URLError as e:
        raise Exception(f"获取 access token 失败：{str(e)}")


def upload_media(access_token, robot_code, media_path, media_type='file'):
    """上传媒体文件到钉钉（使用旧版 API）"""
    if not os.path.exists(media_path):
        raise FileNotFoundError(f"文件不存在：{media_path}")

    # 获取文件 MIME 类型
    mime_type, _ = mimetypes.guess_type(media_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    # 构建 multipart/form-data 请求
    boundary = f'----WebKitFormBoundary{uuid.uuid4().hex}'

    with open(media_path, 'rb') as f:
        file_content = f.read()

    body = []
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(f'Content-Disposition: form-data; name="media"; filename="{os.path.basename(media_path)}"'.encode('utf-8'))
    body.append(f'Content-Type: {mime_type}'.encode('utf-8'))
    body.append(b'')
    body.append(file_content)
    body.append(f'--{boundary}--'.encode('utf-8'))
    body.append(b'')

    body_data = b'\r\n'.join(body)

    # 使用旧版 API（与钉钉插件一致）
    url = f"https://oapi.dingtalk.com/media/upload?access_token={access_token}&type={media_type}&robotCode={urllib.parse.quote(robot_code)}"

    req = urllib.request.Request(
        url,
        data=body_data,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            # 旧版 API 返回 errcode=0 表示成功
            if result.get('errcode') == 0:
                return result.get('media_id')
            else:
                raise Exception(f"钉钉 API 错误：{result.get('errmsg', 'unknown error')}")
    except urllib.error.URLError as e:
        raise Exception(f"上传媒体文件失败：{str(e)}")


def send_media_message(access_token, robot_code, target_id, media_id, media_type='file', is_group=False, file_name=None):
    """发送媒体消息（使用新版 API）"""
    # 使用新版 API（与钉钉插件一致）
    if is_group:
        url = "https://api.dingtalk.com/v1.0/robot/groupMessages/send"
    else:
        url = "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend"

    # 构建消息参数
    if media_type == 'image':
        msg_key = 'sampleImageMsg'
        msg_param = {'photoURL': media_id}
    elif media_type == 'voice':
        msg_key = 'sampleAudio'
        msg_param = {'mediaId': media_id, 'duration': '10'}
    elif media_type == 'video':
        msg_key = 'sampleVideo'
        msg_param = {'picMediaId': media_id}
    else:  # file
        msg_key = 'sampleFile'
        # 必须指定 fileName，否则钉钉会显示为 #fileName#
        msg_param = {'mediaId': media_id, 'fileName': file_name or 'file'}

    payload = {
        'robotCode': robot_code,
        'msgKey': msg_key,
        'msgParam': json.dumps(msg_param)
    }

    if is_group:
        payload['openConversationId'] = target_id
    else:
        payload['userIds'] = [target_id]

    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'x-acs-dingtalk-access-token': access_token
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        raise Exception(f"发送消息失败：{str(e)}")


def detect_media_type(file_path):
    """根据文件扩展名检测媒体类型"""
    ext = os.path.splitext(file_path)[1].lower()

    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    voice_exts = {'.mp3', '.wav', '.amr', '.aac'}
    video_exts = {'.mp4', '.avi', '.mov', '.wmv'}

    if ext in image_exts:
        return 'image'
    elif ext in voice_exts:
        return 'voice'
    elif ext in video_exts:
        return 'video'
    else:
        return 'file'


def detect_group_target(target_id):
    """根据目标 ID 自动判断是否为群聊"""
    return str(target_id).startswith('cid')


def send_media(file_path, target_id, account_id=None, media_type=None, is_group=None, auto_detect_account=True, debug=False, channel_account=None):
    """
    发送媒体文件到钉钉

    Args:
        file_path: 文件路径
        target_id: 目标用户 ID 或群 ID
        account_id: OpenClaw 中的钉钉账号 ID（可选，auto_detect_account=True 时自动检测）
        media_type: 媒体类型 (image/voice/video/file)，None 则自动检测
        is_group: 是否发送到群聊，None 则根据 target_id 自动检测
        auto_detect_account: 是否自动从 OPENCLAW_AGENT_ID 检测账号
        debug: 是否输出调试信息
        channel_account: 从会话上下文传入的账号（direct runtime 模式使用）

    Returns:
        dict: 发送结果
    """
    try:
        # 加载配置
        openclaw_config = load_openclaw_config()

        # 自动检测账号
        if auto_detect_account and not account_id:
            account_id, account_source = detect_account_from_agent_id(
                openclaw_config,
                account_id=account_id,
                channel_account=channel_account
            )
            if debug:
                print(f"[DEBUG] 账号检测来源：{account_source}", file=sys.stderr)
        elif account_id:
            account_source = 'explicit_parameter'
            if debug:
                print(f"[DEBUG] 使用显式指定账号：{account_id}", file=sys.stderr)
        else:
            account_id = 'prd_bot'
            account_source = 'default'
            if debug:
                print(f"[DEBUG] 使用默认账号：{account_id}", file=sys.stderr)

        # 获取钉钉配置
        dingtalk_config = get_dingtalk_config(openclaw_config, account_id)

        # 自动检测媒体类型
        if not media_type:
            media_type = detect_media_type(file_path)

        # 自动检测目标类型，允许命令行通过 --group / --user 覆盖
        if is_group is None:
            is_group = detect_group_target(target_id)

        if debug:
            print(f"[DEBUG] 目标类型：{'group' if is_group else 'user'}", file=sys.stderr)

        # 获取 access token
        access_token = get_access_token(
            dingtalk_config['clientId'],
            dingtalk_config['clientSecret']
        )

        # 上传文件
        media_id = upload_media(
            access_token,
            dingtalk_config['robotCode'],
            file_path,
            media_type
        )

        if not media_id:
            return {'ok': False, 'error': '上传文件失败，未获取到 mediaId'}

        # 发送消息
        result = send_media_message(
            access_token,
            dingtalk_config['robotCode'],
            target_id,
            media_id,
            media_type,
            is_group,
            os.path.basename(file_path)
        )

        return {
            'ok': True,
            'mediaId': media_id,
            'result': result,
            'file': os.path.basename(file_path),
            'target': target_id,
            'type': media_type,
            'isGroup': is_group,
            'targetKind': 'group' if is_group else 'user',
            'account': account_id,
            'accountSource': account_source  # 添加账号来源，便于调试
        }

    except ValueError as e:
        # 配置错误
        return {'ok': False, 'error': f'配置错误：{str(e)}'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(json.dumps({
            'error': '用法：python send_media.py <文件路径> <目标 ID> [账号 ID] [媒体类型] [--group|--user] [--debug]',
            'example': 'python send_media.py /path/to/file.pdf 300523656829570034 prd_bot file --user',
            'note': '默认会根据目标 ID 自动判断：cid 开头视为群聊；可用 --group / --user 显式覆盖',
            'env': {
                'OPENCLAW_AGENT_ID': '当前 Agent ID（用于自动检测账号）',
                'OPENCLAW_ACCOUNT_ID': '直接指定钉钉账号 ID（优先级最高）',
                'DINGTALK_CLIENTID': '直接指定 clientId（优先级最高）',
                'DINGTALK_CLIENTSECRET': '直接指定 clientSecret（优先级最高）'
            }
        }, ensure_ascii=False))
        sys.exit(1)

    file_path = sys.argv[1]
    target_id = sys.argv[2]

    # 解析可选参数
    account_id = None
    media_type = None
    debug = False
    is_group = None
    positionals = []

    for arg in sys.argv[3:]:
        if arg in ['--debug', '-d']:
            debug = True
        elif arg == '--group':
            is_group = True
        elif arg == '--user':
            is_group = False
        else:
            positionals.append(arg)

    if len(positionals) > 0:
        arg = positionals[0]
        if arg in ['image', 'voice', 'video', 'file']:
            media_type = arg
        else:
            account_id = arg

    if len(positionals) > 1:
        arg = positionals[1]
        if arg in ['image', 'voice', 'video', 'file']:
            media_type = arg
        elif account_id is None:
            account_id = arg
        else:
            print(json.dumps({
                'ok': False,
                'error': f'无法解析参数：{arg}'
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

    if len(positionals) > 2:
        print(json.dumps({
            'ok': False,
            'error': '位置参数过多，请使用：<文件路径> <目标 ID> [账号 ID] [媒体类型] [--group|--user] [--debug]'
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 输出调试信息
    if debug:
        print(f"[DEBUG] 文件：{file_path}", file=sys.stderr)
        print(f"[DEBUG] 目标：{target_id}", file=sys.stderr)
        print(f"[DEBUG] OPENCLAW_AGENT_ID={os.environ.get('OPENCLAW_AGENT_ID', '未设置')}", file=sys.stderr)
        print(f"[DEBUG] OPENCLAW_ACCOUNT_ID={os.environ.get('OPENCLAW_ACCOUNT_ID', '未设置')}", file=sys.stderr)
        if is_group is None:
            print(f"[DEBUG] 目标类型自动检测：{'group' if detect_group_target(target_id) else 'user'}", file=sys.stderr)
        else:
            print(f"[DEBUG] 目标类型显式指定：{'group' if is_group else 'user'}", file=sys.stderr)

    # 自动检测账号
    auto_detect = account_id is None

    result = send_media(
        file_path,
        target_id,
        account_id,
        media_type,
        is_group=is_group,
        auto_detect_account=auto_detect,
        debug=debug
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))