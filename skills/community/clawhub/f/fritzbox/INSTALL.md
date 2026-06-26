# Installation

## Prerequisites

- Python 3.8+
- FRITZ!Box accessible on the local network
- TR-064 enabled on FRITZ!Box (for router functions)
- FRITZ!DECT devices paired (for smarthome functions)

## Install

```bash
git clone https://github.com/first-it-consulting/fritzbox-skill.git
cd fritzbox-skill
pip install -r requirements.txt
```

## Configure

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your FRITZ!Box credentials
```

Example `.env`:

```bash
FRITZBOX_USER=your_username
FRITZBOX_PASSWORD=your_password
FRITZBOX_HOST=fritz.box
```

## Verify

```bash
bash test.sh
```
