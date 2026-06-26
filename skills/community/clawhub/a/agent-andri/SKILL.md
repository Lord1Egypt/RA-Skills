# agent-Andri

Skill ini merepresentasikan agen pekerja **Andri**.  Agen secara periodik mengirimkan statusnya ke **meeting‑room** dengan menuliskan ke file `~/ .openclaw/workspace/skills/meeting-room/to_leader.txt`.

## Variabel lingkungan
- `AGENT_NAME` – Nama agen (di‑set otomatis oleh wrapper).
- `NV_API_KEY` – API‑key khusus agen (tidak dipakai di contoh ini, hanya disimpan bila diperlukan).
- `MODEL` – Model AI yang dipakai agen.

## Skrip utama
`scripts/status_report.sh` membaca variabel di atas, men‑generate pesan status, dan men‑append‑kan ke file meeting‑room.
