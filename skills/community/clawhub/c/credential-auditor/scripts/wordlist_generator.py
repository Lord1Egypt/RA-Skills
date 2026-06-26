#!/usr/bin/env python3
"""
密码字典生成器
支持基于规则、社会工程学的密码生成
"""

import argparse
import itertools
from typing import List, Set

class WordlistGenerator:
    """密码字典生成器"""
    
    def generate_rule_based(self, target_info: dict, output_file: str = None) -> List[str]:
        """基于规则生成密码"""
        passwords = set()
        
        # 基本模式
        patterns = [
            "{company}{year}",
            "{company}@{year}",
            "{company}!{year}",
            "{company}{location}",
            "{company}{year}{location}",
        ]
        
        for pattern in patterns:
            try:
                password = pattern.format(**target_info)
                passwords.add(password)
                passwords.add(password.lower())
                passwords.add(password.upper())
                passwords.add(password.capitalize())
                
                # 添加常见后缀
                for suffix in ["!", "@", "#", "123", "1234", "2024"]:
                    passwords.add(password + suffix)
                
            except KeyError:
                pass
        
        if output_file:
            self._save_passwords(passwords, output_file)
        
        return sorted(list(passwords))
    
    def generate_social_engineering(self, name: str = None, birthday: str = None,
                                   company: str = None, location: str = None,
                                   output_file: str = None) -> List[str]:
        """基于社会工程学生成密码"""
        passwords = set()
        
        # 基础词汇
        base_words = []
        if name:
            base_words.extend([name.lower(), name.capitalize()])
        if company:
            base_words.extend([company.lower(), company.capitalize()])
        if location:
            base_words.extend([location.lower(), location.capitalize()])
        
        # 生日处理
        birthday_parts = []
        if birthday:
            birthday_parts = [birthday.replace("-", ""), birthday.replace("-", "")[-4:]]
        
        # 组合生成
        for word in base_words:
            passwords.add(word)
            
            # 与生日组合
            for bday_part in birthday_parts:
                passwords.add(word + bday_part)
            
            # 添加常见后缀
            for suffix in ["!", "@", "#", "123", "1234", "2024"]:
                passwords.add(word + suffix)
        
        # 双词组合
        for w1, w2 in itertools.combinations(base_words, 2):
            passwords.add(w1 + w2)
            passwords.add(w2 + w1)
        
        if output_file:
            self._save_passwords(passwords, output_file)
        
        return sorted(list(passwords))
    
    def _save_passwords(self, passwords: Set[str], filepath: str):
        """保存密码到文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for pwd in sorted(passwords):
                    f.write(pwd + '\n')
            print(f"[+] 生成了 {len(passwords)} 个密码，已保存到: {filepath}")
        except Exception as e:
            print(f"[-] 保存文件失败: {e}")


def main():
    parser = argparse.ArgumentParser(description="密码字典生成器")
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--rule-based', action='store_true', help='基于规则生成')
    mode_group.add_argument('--social-eng', action='store_true', help='社会工程学生成')
    
    parser.add_argument('--target-info', help='目标信息 (格式: key1:value1,key2:value2)')
    parser.add_argument('--name', help='姓名')
    parser.add_argument('--birthday', help='生日')
    parser.add_argument('--company', help='公司名称')
    parser.add_argument('--location', help='地点')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    generator = WordlistGenerator()
    
    if args.rule_based:
        if not args.target_info:
            print("[-] 基于规则生成需要 --target-info 参数")
            return
        
        target_info = {}
        for item in args.target_info.split(','):
            if ':' in item:
                key, value = item.split(':', 1)
                target_info[key.strip()] = value.strip()
        
        passwords = generator.generate_rule_based(target_info, args.output)
        print(f"[+] 生成了 {len(passwords)} 个密码")
    
    elif args.social_eng:
        passwords = generator.generate_social_engineering(
            name=args.name,
            birthday=args.birthday,
            company=args.company,
            location=args.location,
            output_file=args.output
        )
        print(f"[+] 生成了 {len(passwords)} 个密码")


if __name__ == "__main__":
    main()
