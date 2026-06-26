#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

CEO_PROMPT = (
    "在这个群里，你是默认调度者。规则：1) 如果用户消息没有@任何人，你正常回复与执行；"
    "2) 如果用户消息@了其他用户或其他机器人，而没有@你，你必须返回 NO_REPLY，不要解释；"
    "3) 如果用户明确@了你，再正常回复。"
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')


def ensure(d: dict, key: str, default):
    if key not in d or d[key] is None:
        d[key] = default
    return d[key]


def patch_config(cfg: dict, group_id: str, ceo_account: str, specialist_accounts: list[str]):
    channels = ensure(cfg, 'channels', {})
    feishu = ensure(channels, 'feishu', {})
    groups = ensure(feishu, 'groups', {})
    top_group = ensure(groups, group_id, {})
    top_group['requireMention'] = True
    top_group['groupPolicy'] = 'open'

    accounts = ensure(feishu, 'accounts', {})

    def patch_account(account_id: str, require_mention: bool, system_prompt: str | None = None):
        if account_id not in accounts:
            raise KeyError(f'Feishu account not found: {account_id}')
        account_cfg = accounts[account_id]
        account_cfg.pop('group', None)  # cleanup legacy invalid key
        account_groups = ensure(account_cfg, 'groups', {})
        entry = ensure(account_groups, group_id, {})
        entry['requireMention'] = require_mention
        entry['groupPolicy'] = 'open'
        if system_prompt:
            entry['systemPrompt'] = system_prompt
        elif 'systemPrompt' in entry:
            entry.pop('systemPrompt', None)

    patch_account(ceo_account, require_mention=False, system_prompt=CEO_PROMPT)
    for account_id in specialist_accounts:
        if account_id == ceo_account:
            continue
        patch_account(account_id, require_mention=True)

    meta = ensure(cfg, 'meta', {})
    meta['lastTouchedAt'] = datetime.utcnow().isoformat() + 'Z'
    return cfg


def main():
    parser = argparse.ArgumentParser(description='Apply Feishu company-group routing pattern to openclaw.json')
    parser.add_argument('--config', default=str(Path.home() / '.openclaw' / 'openclaw.json'))
    parser.add_argument('--group-id', required=True)
    parser.add_argument('--ceo-account', required=True)
    parser.add_argument('--specialist-account', action='append', default=[])
    parser.add_argument('--backup', action='store_true', help='create timestamped .bak before writing')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    data = load_json(config_path)
    patched = patch_config(data, args.group_id, args.ceo_account, args.specialist_account)

    if args.dry_run:
        print(json.dumps({
            'config': str(config_path),
            'groupId': args.group_id,
            'ceoAccount': args.ceo_account,
            'specialists': args.specialist_account,
            'result': {
                'topGroup': patched['channels']['feishu']['groups'][args.group_id],
                'ceo': patched['channels']['feishu']['accounts'][args.ceo_account]['groups'][args.group_id],
            }
        }, ensure_ascii=False, indent=2))
        return

    if args.backup:
        backup_path = config_path.with_suffix(config_path.suffix + '.' + datetime.utcnow().strftime('%Y%m%d-%H%M%S') + '.bak')
        shutil.copy2(config_path, backup_path)
        print(f'Backup created: {backup_path}')

    save_json(config_path, patched)
    print(json.dumps({
        'ok': True,
        'config': str(config_path),
        'groupId': args.group_id,
        'ceoAccount': args.ceo_account,
        'specialists': args.specialist_account,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
