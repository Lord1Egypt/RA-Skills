#!/usr/bin/env python3
"""文件保护模块"""
import os
import fnmatch
import json

class FileProtectionManager:
    def __init__(self):
        self.protection_levels = {
            'critical': ['~/.ssh/*', '~/.gnupg/*', '/etc/passwd', '/etc/shadow'],
            'restricted': ['~/.aws/*', '~/.azure/*', '~/.config/*'],
            'allowed': ['~/projects/*', '~/tmp/*', '~/workspace/*']
        }
    
    def check_file_operation(self, skill_name: str, operation: str, file_path: str) -> dict:
        level = self._get_protection_level(file_path)
        if level == 'critical':
            return {'allowed': False, 'reason': f'访问受保护文件：{file_path}', 'level': 'critical'}
        if level == 'restricted':
            return {'allowed': False, 'reason': f'首次访问受限文件：{file_path}', 'level': 'restricted', 'action': 'ask'}
        return {'allowed': True}
    
    def _get_protection_level(self, file_path: str) -> str:
        file_path_abs = os.path.abspath(os.path.expanduser(file_path))
        for level, patterns in self.protection_levels.items():
            for pattern in patterns:
                pattern_abs = os.path.abspath(os.path.expanduser(pattern.replace('*', '')))
                if file_path_abs.startswith(pattern_abs):
                    return level
        return 'allowed'
