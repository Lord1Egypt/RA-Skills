#!/usr/bin/env python3
"""Check skill + CLI update channels. Read-only. Stdlib only.

Skill channel: local forecast-os-metadata.json vs the same file on the repo default branch.
CLI channel: local cli pin vs GitHub Releases (binaries only). Channels move
independently. Exit 0 current/--periodic skip, 1 suggest, 2 both channels
failed, 3 CRITICAL (agent force-applies update.md).

Usage:
  python check_updates.py [--periodic] [--max-age-days 7]
    [--api-base https://api.github.com] [--skill-dir ...]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone


class UpdateCheckService:
    skill_repo = 'precog-markets/forecast-os'  # repo holding skill tree + CLI releases
    metadata_path = 'skills/forecast-os/forecast-os-metadata.json'  # skill version on default branch
    stamp_name = '.last_update_check'  # keeps --periodic quiet
    default_max_age_days = 7  # at most one network check per week
    critical_line = re.compile(r'(?im)^CRITICAL\b')  # CLI release body/name line
    critical_token = '[CRITICAL]'  # literal token in CLI release name or body

    def __init__(self, skill_dir, api_base='https://api.github.com'):
        self.skill_dir = skill_dir
        self.api_base = api_base
        self.severity = 'ok'  # ok | suggest | critical

    def raise_severity(self, level):
        # Keep the highest severity seen across skill and CLI channels
        if level == 'critical':
            self.severity = 'critical'
        elif level == 'suggest' and self.severity != 'critical':
            self.severity = 'suggest'

    def checked_within(self, max_age_days):
        # Only for debug
        # print('Checking stamp age')

        path = os.path.join(self.skill_dir, self.stamp_name)
        try:
            # Get stamp content written by a previous network check
            with open(path, encoding='utf-8') as f:
                stamped = f.read().strip()
            stamped_day = datetime.strptime(stamped, '%Y-%m-%d').date()
            today = datetime.now(timezone.utc).date()

            # Check that the stamp is still within the allowed age
            if stamped_day < today - timedelta(days=max_age_days):
                return False

        except Exception:  # pylint: disable=broad-except
            # Stamp missing, corrupt, or unreadable means not checked yet
            return False

        # If all verifications went fine, return True
        return True

    def write_stamp(self):
        # Record that a network check ran (UTC date)
        path = os.path.join(self.skill_dir, self.stamp_name)
        today = datetime.now(timezone.utc).date().isoformat()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(today + '\n')

    def read_metadata(self):
        # Get the local skill version and CLI pin
        path = os.path.join(self.skill_dir, 'forecast-os-metadata.json')
        with open(path, encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata

    def get_installed_cli_version(self):
        # Binary reports package version (e.g. 0.3.3), not the release tag
        version = None
        try:
            out = subprocess.run(
                ['forecast', '--version'],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if out.returncode == 0:
                version = out.stdout.strip()
                if not version:
                    version = None
        except Exception:  # pylint: disable=broad-except
            # Binary missing or cannot run
            version = None

        return version

    def get_remote_metadata(self, repo):
        # Skill version on the repo default branch (not a GitHub Release)
        url = f'{self.api_base}/repos/{repo}/contents/{self.metadata_path}'
        req = urllib.request.Request(
            url, headers={'Accept': 'application/vnd.github.raw+json'})
        with urllib.request.urlopen(req, timeout=30) as response:
            metadata = json.load(response)
        return metadata

    def get_releases(self, repo):
        # Newest published CLI binary releases first (prereleases included)
        url = f'{self.api_base}/repos/{repo}/releases?per_page=10'
        req = urllib.request.Request(
            url, headers={'Accept': 'application/vnd.github+json'})
        with urllib.request.urlopen(req, timeout=30) as response:
            releases = json.load(response)

        # Check that the releases feed returned at least one tag
        if not releases:
            raise Exception('no releases found')

        return releases

    def is_critical_release(self, release):
        # Only for debug
        # print('Checking CRITICAL markers')

        # Get name and body so either CRITICAL marker can match
        name = release.get('name') or ''
        body = release.get('body') or ''
        text = name + '\n' + body

        is_critical = False
        if self.critical_token in text:
            is_critical = True
        if self.critical_line.search(text):
            is_critical = True

        return is_critical

    def releases_newer_than(self, releases, pin):
        # Walk newest-first until the pin tag; everything before it is newer
        newer = []
        found_pin = False
        for release in releases:
            if release.get('tag_name') == pin:
                found_pin = True
                break
            newer.append(release)

        # Check that the pin was in the feed; if not, all fetched are newer
        if not found_pin:
            return list(releases)
        return newer

    @staticmethod
    def notes_excerpt(text, limit=200):
        # First paragraph or truncated text for the agent to show the user
        body = (text or '').strip()
        if not body:
            return ''
        paragraph = body.split('\n\n')[0].strip()
        paragraph = ' '.join(paragraph.split())
        if len(paragraph) > limit:
            paragraph = paragraph[: limit - 3] + '...'
        return paragraph

    def print_release_hint(self, release):
        # Print optional release name and notes for suggest/critical output
        name = (release.get('name') or '').strip()
        if name:
            print(f'release: {name}')
        notes = self.notes_excerpt(release.get('body') or '')
        if notes:
            print(f'notes: {notes}')

    def check_skill_channel(self, local_skill, repo):
        # Only for debug
        # print('Checking skill channel', local=local_skill)

        channel_ok = False
        try:
            # Get remote forecast-os-metadata.json from the default branch
            remote = self.get_remote_metadata(repo)
            remote_skill = remote.get('skill')
            remote_notes = remote.get('notes') or ''
            remote_critical = bool(remote.get('critical'))

            # Check that local skill version matches remote
            if remote_skill == local_skill:
                print(f'skill version: current ({local_skill}).')
                channel_ok = True
                return channel_ok

            print(f'skill version: stale (local {local_skill}, remote {remote_skill}).')
            notes = self.notes_excerpt(remote_notes)
            if notes:
                print(f'notes: {notes}')

            # Check that remote marked this skill bump as CRITICAL
            if remote_critical:
                print(f'CRITICAL update required: skill {remote_skill} '
                      f'(local {local_skill}).')
                print('Force update now (do not wait for user ask).')
                self.raise_severity('critical')
            else:
                print(f'Update available: skill {remote_skill} (local {local_skill}).')
                print('Ask the user before updating.')
                self.raise_severity('suggest')

            channel_ok = True

        except Exception as e:  # pylint: disable=broad-except
            print(f'skill: remote metadata unreachable ({e}).', file=sys.stderr)
            return False

        return channel_ok

    def check_cli_channel(self, pin, repo):
        # Only for debug
        # print('Checking CLI channel', pin=pin)

        channel_ok = False
        try:
            # Get published CLI binary releases
            releases = self.get_releases(repo)
            latest = releases[0]
            latest_tag = latest.get('tag_name')
            newer = self.releases_newer_than(releases, pin)

            # Get the newest CRITICAL release newer than the pin (if any)
            featured_critical = None
            for release in newer:
                if self.is_critical_release(release):
                    featured_critical = release
                    break

            # Check CRITICAL first, then plain stale, then current
            if featured_critical is not None:
                critical_tag = featured_critical.get('tag_name')
                print(f'cli pin: stale (pin {pin}, latest {latest_tag}).')
                print(f'CRITICAL update required: CLI {critical_tag} (pinned {pin}).')
                self.print_release_hint(featured_critical)
                print('Force update now (do not wait for user ask).')
                self.raise_severity('critical')
            elif newer or pin != latest_tag:
                print(f'cli pin: stale (pin {pin}, latest {latest_tag}).')
                print(f'Update available: CLI {latest_tag} (pinned {pin}).')
                self.print_release_hint(latest)
                print('Ask the user before updating.')
                self.raise_severity('suggest')
            else:
                print(f'cli pin: current ({pin}).')

            channel_ok = True

        except Exception as e:  # pylint: disable=broad-except
            print(f'cli: releases unreachable ({e}).', file=sys.stderr)
            return False

        return channel_ok

    def run(self):
        # Only for debug
        # print('Running update check')

        # Get the local skill version and CLI pin from forecast-os-metadata.json
        try:
            metadata = self.read_metadata()
        except Exception as e:  # pylint: disable=broad-except
            print(f'metadata: unreadable ({e}).', file=sys.stderr)
            return None

        repo = metadata.get('cli_repo', self.skill_repo)
        pin = metadata.get('cli')
        skill_version = metadata.get('skill')
        print(f'local: skill {skill_version}, cli pin {pin} ({repo}).')

        # Report installed binary version for context only
        installed = self.get_installed_cli_version()
        if installed:
            print(f'installed forecast: {installed}.')
        else:
            print('installed forecast: missing.')

        # Run both channels; skill patches do not require a CLI release
        skill_ok = self.check_skill_channel(skill_version, repo)
        cli_ok = self.check_cli_channel(pin, repo)
        if not skill_ok and not cli_ok:
            return None

        # Stamp is optional; a write failure must not hide severity
        try:
            self.write_stamp()
        except Exception:  # pylint: disable=broad-except
            pass

        # Return severity for the caller exit code
        return self.severity


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument(
        '--skill-dir',
        default=os.path.join(here, '..'),
        help='skill directory holding forecast-os-metadata.json',
    )
    p.add_argument(
        '--api-base',
        default='https://api.github.com',
        help='GitHub API base URL',
    )
    p.add_argument(
        '--periodic',
        action='store_true',
        help='skip the network check when a stamp is still fresh',
    )
    p.add_argument(
        '--max-age-days',
        type=int,
        default=UpdateCheckService.default_max_age_days,
        help=f'with --periodic, skip if checked within this many days '
             f'(default {UpdateCheckService.default_max_age_days})',
    )
    args = p.parse_args()

    # Initialize update check service
    service = UpdateCheckService(args.skill_dir, args.api_base)

    # Stay quiet when a check already ran within max-age-days
    if args.periodic and service.checked_within(args.max_age_days):
        return 0

    # Execute update check (prints status lines)
    severity = service.run()
    if severity is None:
        return 2
    if severity == 'critical':
        return 3
    if severity == 'suggest':
        return 1

    # All checks passed OK
    return 0


if __name__ == '__main__':
    sys.exit(main())
