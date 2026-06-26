#!/usr/bin/env python3
"""
Error handling utilities for ChaoJi CLI.

Provides standardized error response format and error code mappings.
"""

import os


# Error code to error type mapping
ERROR_CODE_MAP = {
    # Authentication errors
    'AUTH_001': 'CREDENTIALS_MISSING',
    'AUTH_002': 'AUTH_ERROR',
    'AUTH_003': 'TOKEN_EXPIRED',
    
    # Input errors
    'INPUT_001': 'INPUT_ERROR',
    'INPUT_002': 'INPUT_ERROR',
    'INPUT_003': 'VALIDATION_ERROR',
    
    # API errors
    'API_001': 'API_ERROR',
    'API_002': 'API_ERROR',
    'API_500': 'API_ERROR',
    'API_TIMEOUT': 'TIMEOUT',
    
    # Resource errors
    'RESOURCE_001': 'RESOURCE_NOT_FOUND',
    'QUOTA_001': 'QUOTA_EXCEEDED',
    
    # Runtime errors
    'RUNTIME_001': 'RUNTIME_ERROR',
    'RUNTIME_002': 'RUNTIME_ERROR',
}


# Default error messages by error type
ERROR_MESSAGES = {
    'CREDENTIALS_MISSING': {
        'error_name': '凭证缺失',
        'user_hint': '检测到未配置潮际 API 凭证',
        'next_action': '请设置环境变量 CHAOJI_AK 和 CHAOJI_SK，或创建凭证文件 ~/.chaoji/credentials.json',
    },
    'AUTH_ERROR': {
        'error_name': '认证失败',
        'user_hint': 'API 凭证验证失败，请检查 AK/SK 是否正确',
        'next_action': '请重新获取凭证并更新配置',
    },
    'INPUT_ERROR': {
        'error_name': '输入错误',
        'user_hint': '输入参数有误',
        'next_action': '请检查输入参数格式和必填项',
    },
    'API_ERROR': {
        'error_name': 'API 调用失败',
        'user_hint': '调用潮际 API 时发生错误',
        'next_action': '请稍后重试，如持续失败请联系技术支持',
    },
    'TIMEOUT': {
        'error_name': '任务超时',
        'user_hint': '任务执行超时，可能由于服务器繁忙',
        'next_action': '请稍后重试或减少并发任务数',
    },
    'QUOTA_EXCEEDED': {
        'error_name': '配额不足',
        'user_hint': '账户余额或配额不足',
        'next_action': '请充值或购买更多配额',
    },
    'RUNTIME_ERROR': {
        'error_name': '运行时错误',
        'user_hint': '程序执行过程中发生异常',
        'next_action': '请检查环境和依赖后重试',
    },
    'RESOURCE_NOT_FOUND': {
        'error_name': '资源不存在',
        'user_hint': '请求的资源（图片、视频等）不存在或无法访问',
        'next_action': '请检查资源 URL 或路径是否正确',
    },
}


def build_error_response(error_type=None, error_code=None, error_name=None, 
                         user_hint=None, next_action=None, action_url=None,
                         action_label=None, action_link=None):
    """
    Build a standardized error response.
    
    Args:
        error_type: Error type (e.g., CREDENTIALS_MISSING, AUTH_ERROR)
        error_code: Error code (e.g., AUTH_001, API_500)
        error_name: Error name in Chinese (e.g., "凭证缺失")
        user_hint: User-friendly error explanation
        next_action: Suggested repair action
        action_url: Action URL (if applicable)
        action_label: Action button label
        action_link: Markdown formatted action link
        
    Returns:
        Dictionary with standardized error response format
    """
    response = {
        'ok': False,
    }
    
    # Add error details if provided
    if error_type:
        response['error_type'] = error_type
    
    if error_code:
        response['error_code'] = error_code
    
    if error_name:
        response['error_name'] = error_name
    
    if user_hint:
        response['user_hint'] = user_hint
    
    if next_action:
        response['next_action'] = next_action
    
    if action_url:
        response['action_url'] = action_url
    
    if action_label:
        response['action_label'] = action_label
    
    if action_link:
        response['action_link'] = action_link
    
    # Auto-fill missing fields based on error_type
    if error_type and error_type in ERROR_MESSAGES:
        defaults = ERROR_MESSAGES[error_type]
        if not error_name:
            response['error_name'] = defaults['error_name']
        if not user_hint:
            response['user_hint'] = defaults['user_hint']
        if not next_action:
            response['next_action'] = defaults['next_action']
    
    return response


def infer_error_code_from_text(text):
    """
    Infer error code from error message text.
    
    Args:
        text: Error message text
        
    Returns:
        Inferred error code or None
    """
    if not text:
        return None
    text_lower = text.lower()
    
    if 'credential' in text_lower or 'access key' in text_lower or 'secret key' in text_lower:
        return 'AUTH_001'
    elif 'auth' in text_lower or 'unauthorized' in text_lower:
        return 'AUTH_002'
    elif 'timeout' in text_lower or 'timed out' in text_lower:
        return 'API_TIMEOUT'
    elif 'not found' in text_lower or '404' in text_lower:
        return 'RESOURCE_001'
    elif 'quota' in text_lower or 'balance' in text_lower or 'insufficient' in text_lower:
        return 'QUOTA_001'
    elif 'invalid' in text_lower or 'validation' in text_lower:
        return 'INPUT_003'
    elif 'server' in text_lower or '500' in text_lower:
        return 'API_500'
    
    return None


def get_action_url_from_env():
    """Get action URL from environment variables."""
    return os.environ.get('CHAOJI_CONSOLE_URL', 'https://open.chaoji.com/console')


def get_order_url_from_env():
    """Get order URL from environment variables."""
    return os.environ.get('CHAOJI_ORDER_URL', 'https://open.chaoji.com/order')


def format_action_link(label, url):
    """Format action link as markdown."""
    return f'[{label}]({url})'
