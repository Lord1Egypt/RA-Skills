#!/usr/bin/env python3
import json
from pathlib import Path


def setup_config():
    skill_dir = Path(__file__).parent.parent
    local_dir = skill_dir / 'local'
    local_dir.mkdir(exist_ok=True)
    config_file = local_dir / 'config.json'

    print('=== 抖音学习流水线配置向导 ===\n')

    config = {}
    if config_file.exists():
        config = json.loads(config_file.read_text(encoding='utf-8'))
        print('检测到已有本地配置，将更新缺失项。\n')

    if not config.get('siliconflow_api_key'):
        key = input('请输入 SiliconFlow API Key: ').strip()
        if key:
            config['siliconflow_api_key'] = key
            print('✓ 已保存 SiliconFlow API Key（本地配置）\n')

    if not config.get('feishu_doc_token'):
        token = input('飞书文档 token（可选，直接回车跳过）: ').strip()
        if token:
            config['feishu_doc_token'] = token
            print('✓ 已保存飞书文档 token（本地配置）\n')

    config_file.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'本地配置已保存到: {config_file}\n')

    downloader_dir = skill_dir / 'assets' / 'douyin-downloader'
    cookie_config = downloader_dir / 'config.yml'
    if not cookie_config.exists():
        print('=== 抖音 Cookie 配置 ===')
        print('douyin-downloader 需要配置抖音 Cookie 才能下载视频。\n')
        print('步骤:')
        print('1. 浏览器打开抖音网页版并登录')
        print('2. 按 F12 打开开发者工具')
        print('3. 切换到 Application/存储 → Cookies')
        print('4. 复制以下 Cookie 字段名对应的值:')
        print('   - msToken')
        print('   - ttwid')
        print('   - odin_tt')
        print('   - passport_csrf_token')
        print('   - sid_guard\n')
        print(f'5. 编辑配置文件: {cookie_config}')
        print('   参考: config.yml.example\n')

    print('=== 配置完成 ===')
    print('现在可以开始使用了！')


if __name__ == '__main__':
    setup_config()
