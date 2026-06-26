#!/usr/bin/env python3
"""
Email Pro Optimized - 高性能邮件工具
支持: QQ邮箱、Gmail、Outlook
"""

import json
import sys
import argparse
from pathlib import Path
from providers import get_provider

CONFIG_FILE = Path.home() / '.openclaw' / 'credentials' / 'email-accounts.json'

class EmailManager:
    def __init__(self, account='qq_3421'):
        self.account_name = account
        self.config = self._load_config(account)
        self.provider = get_provider(self.config)
    
    def _load_config(self, account):
        if not CONFIG_FILE.exists():
            raise FileNotFoundError(f"配置文件不存在: {CONFIG_FILE}")
        
        with open(CONFIG_FILE, 'r') as f:
            accounts = json.load(f)
        
        if account not in accounts:
            raise ValueError(f"账户不存在: {account}")
        
        return accounts[account]
    
    def check_emails(self, limit=10, unread_only=False, mailbox='INBOX'):
        """检查邮件"""
        results = self.provider.check_emails(limit, unread_only, mailbox)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return results
    
    def fetch_email(self, uid, mailbox='INBOX'):
        """获取完整邮件"""
        result = self.provider.fetch_email(uid, mailbox)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    
    def search_emails(self, query='', limit=20, mailbox='INBOX'):
        """搜索邮件"""
        results = self.provider.search_emails(query, limit, mailbox)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return results
    
    def send_email(self, to, subject, body, html=False, attachments=None):
        """发送邮件"""
        success = self.provider.send_email(to, subject, body, html, attachments)
        if success:
            print(f"✅ 邮件已发送给 {to}")
        else:
            print(f"❌ 发送邮件失败")
        return success
    
    def list_accounts(self):
        """列出所有账户"""
        with open(CONFIG_FILE, 'r') as f:
            accounts = json.load(f)
        
        print("\n📧 已配置的邮箱账户:\n")
        for name, config in accounts.items():
            email = config.get('email')
            provider = config.get('provider', 'imap')
            status = config.get('status', '⚠️ 未知')
            note = config.get('note', '')
            print(f"  {name:15} | {email:25} | {provider:8} | {status:10} | {note}")
        print()

def main():
    parser = argparse.ArgumentParser(description='📧 Email Pro Optimized - 高性能邮件工具')
    parser.add_argument('--account', default='qq_3421', help='账户名称')
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    check_parser = subparsers.add_parser('check', help='检查邮件')
    check_parser.add_argument('--limit', type=int, default=10, help='限制数量')
    check_parser.add_argument('--unread', action='store_true', help='仅未读')
    check_parser.add_argument('--mailbox', default='INBOX', help='邮箱')
    
    fetch_parser = subparsers.add_parser('fetch', help='获取邮件')
    fetch_parser.add_argument('uid', help='邮件 UID')
    fetch_parser.add_argument('--mailbox', default='INBOX', help='邮箱')
    
    search_parser = subparsers.add_parser('search', help='搜索邮件')
    search_parser.add_argument('query', help='搜索关键词')
    search_parser.add_argument('--limit', type=int, default=20, help='限制数量')
    search_parser.add_argument('--mailbox', default='INBOX', help='邮箱')
    
    send_parser = subparsers.add_parser('send', help='发送邮件')
    send_parser.add_argument('--to', required=True, help='收件人')
    send_parser.add_argument('--subject', required=True, help='主题')
    send_parser.add_argument('--body', required=True, help='正文')
    send_parser.add_argument('--html', action='store_true', help='HTML 格式')
    send_parser.add_argument('--attach', nargs='+', help='附件')
    
    subparsers.add_parser('list-accounts', help='列出账户')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        manager = EmailManager(args.account)
        
        if args.command == 'check':
            manager.check_emails(args.limit, args.unread, args.mailbox)
        
        elif args.command == 'fetch':
            manager.fetch_email(args.uid, args.mailbox)
        
        elif args.command == 'search':
            manager.search_emails(args.query, args.limit, args.mailbox)
        
        elif args.command == 'send':
            manager.send_email(args.to, args.subject, args.body, args.html, args.attach)
        
        elif args.command == 'list-accounts':       manager.list_accounts()
    
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
