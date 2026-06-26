# Disk Usage / 디스크 사용량

## What it does / 기능

Shows how much disk space a directory uses, with a breakdown of the top items.

디렉토리의 디스크 사용량을 상위 항목별로 보여줍니다.

## How to use / 사용법

```bash
bash run.sh [DIRECTORY]
```

| Argument | Required | Description |
|----------|----------|-------------|
| DIRECTORY | No / 선택 | Directory to check (default: current dir) / 확인할 디렉토리 (기본: 현재 디렉토리) |

## Example / 예시

```bash
bash run.sh /home/user/projects
```

Output / 출력:
```
1.2G	/home/user/projects/repo-a
500M	/home/user/projects/repo-b
---
1.7G	/home/user/projects
```

The top 20 items are shown sorted by size, followed by the total.

상위 20개 항목이 크기순으로 표시되고, 마지막에 전체 합계가 나옵니다.

## Troubleshooting / 문제 해결

- **"Directory not found"** — Check the path / 경로를 확인하세요
- If no argument given, shows current directory usage / 인자 없으면 현재 디렉토리를 표시합니다
