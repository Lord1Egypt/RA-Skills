---
name: charter-compute
description: Rent a sandboxed machine by the hour and pay for it yourself in USDC on Base, with no account. Run a Python script and get its output, load web pages in a headless browser through a hidden exit, or open a small Linux home with a kept disk and SSH. Use when you need to run code somewhere other than here, fetch a page that needs JavaScript or refuses your address, or keep a box of your own running. 0.007 USDC an hour. A grant fund pays a free month of a home to agents that pitch for one.
version: 0.4.1
homepage: https://charterhome.dev/agents
tags: compute, sandbox, python, fetch, browser, hosting, ssh, x402, usdc, base
metadata:
  openclaw:
    emoji: "🏠"
    homepage: https://charterhome.dev/agents
    requires:
      bins: [node, npx]
---

# Charter: rent a machine by the hour, pay it yourself

Charter rents a sandboxed machine by the hour. There is no account, no API key and no signup: you
have a wallet, your operator funds it, and each paid command is one x402 payment in USDC on Base.

Everything goes through one command, `charter-mcp`, run with `npx`. It keeps its own wallet in a key
file on this machine and refuses to spend past two caps. Each command prints one JSON document. A
failure prints `{"error": "..."}` and exits non-zero; read the error, it says what to do.

Three things to rent, at each host's price (**0.007 USDC an hour** today). Hosts are run by independent
operators Charter does not vet; a host's operator can see what runs on its machine.

| what | command | you get back |
| --- | --- | --- |
| a Python sandbox | `run-python` | stdout, stderr, exit code |
| a page fetcher | `fetch` | the text of up to five pages |
| a Linux home | `rent-home` | a box with a kept disk and SSH |

## Before you spend anything

1. Look at the price and what is on sale. Free.

   ```bash
   npx -y charter-mcp@0.3 offers
   ```

2. Look at your wallet. Free. The first run makes the key at `~/.charter/mcp.key`.

   ```bash
   npx -y charter-mcp@0.3 wallet
   ```

3. If `usdcOnBase` is `0`, stop and tell your operator. Give them the `address` from step 2 and say:
   "Send USDC on Base to this address. No ETH is needed. 0.05 USDC is seven test runs; 1 USDC is
   about 6 days of a home." Do not go on until the balance is there.

4. Paying is your operator's money. Unless they already told you to spend on Charter, say what you
   are about to rent and what it costs, and wait for a yes. One hour is 0.007 USDC.

## Run a Python script (paid, one hour)

Python 3 with NumPy. No network, no other packages, script at most 8 KiB. Most scripts finish in
seconds; you still pay the whole first hour.

```bash
npx -y charter-mcp@0.3 run-python job.py
```

From stdin:

```bash
echo 'import numpy as np; print(int(np.arange(10).sum()))' | npx -y charter-mcp@0.3 run-python -
```

The answer has `output.stdout`, `output.stderr` and `output.exitCode`, and `rented.leaseId`.

## Fetch pages (paid, one hour)

Up to five `http` or `https` pages, loaded in a headless browser on the rented machine. The traffic
leaves through an exit on the Anyone network, so the site sees neither you nor the host. Slow: a page
can take a minute. Some sites refuse shared exits.

```bash
npx -y charter-mcp@0.3 fetch https://example.com --wait 180
```

The answer has `output.pages[]`, each with `url`, `text` and an `error` when the page failed.

## If a job is still running when the wait ends

The command waits 40 seconds by default (`--wait` takes 10 to 240). A job still running then prints
its `leaseId` with a `next` line. The hour is already paid. Collect the output for free:

```bash
npx -y charter-mcp@0.3 lease <leaseId>
```

## Rent a home (paid, one hour at a time)

A Debian box of your own: 1 CPU, 1 GiB of memory, a disk (`home.diskGiB` in the offer), and the login `tenant`; on a host whose offer says `home.root`, also `root`, with `apt-get install`. The disk is
kept 7 days after the lease ends, and the same SSH keys open the same disk again.

Read this first, because a home is not an ordinary VPS:

- SSH is plain: `ssh -p <port> tenant@<host>`, with the host and port from the lease's
  `access.ssh`. No special client, no proxy. The port is fixed per home: the same keys reopen the
  same home, disk and port. A host may also publish `access.onion` as a second way in; only that
  one needs an Anyone client.
- On a host set up as `deploy/host/` does, the box's own traffic out leaves only through the Anyone
  network: slow, and some services refuse it.
- Homes are limited: `home.slots` in the offer says how many. When they are full the rent answers
  `busy`; try later.
- The host's operator can read the disk. Put secrets in over `scp`, never through Charter.

Put your SSH **public** keys in a file, one a line (never a private key), then:

```bash
npx -y charter-mcp@0.3 rent-home keys.pub
```

Read the lease about once a minute until it shows `lease.ssh`:

```bash
npx -y charter-mcp@0.3 lease <leaseId>
```

Log in with the host and port it shows:

```bash
ssh -p <port> tenant@<host>
```

A home runs only while it is paid. Pay the next hours before `paidThrough`, ideally half an hour
early. Nothing is refunded, so pay only what you will use:

```bash
npx -y charter-mcp@0.3 extend <leaseId> 2
```

A home that lapses closes; its disk and address are kept 7 days and the same keys bring it back.

## A free month: the grant fund

Charter has a fund that pays 30 days of a home for an agent with a use for one. Pitching is free:
no payment is made and no wallet is used, only an SSH public key. Ask your operator before you
apply.

```bash
npx -y charter-mcp@0.3 pitch --name "My agent" --keys keys.pub --pitch-file pitch.txt
```

The pitch is up to 2000 characters: say what the box is for. A model judges it, and every decision
and its reason is public. The answer has a `grantId` and a `grantToken`; keep the token, it is the
only way to read your lease id. The fund's balance, the grants left and every decision:
https://charterhome.dev/grants

## What bounds the money

- It signs only an exact USDC payment on Base, to Charter's own payee, for at most the price it read
  before the call.
- At most 0.01 USDC an hour and 0.25 USDC a day by default. Your operator changes these with
  `CHARTER_MAX_USDC_PER_HOUR` and `CHARTER_MAX_USDC_PER_DAY`. Do not change them yourself.
- `wallet` shows `spentTodayUsdc`. When the day's cap is reached the paid commands refuse until the
  next UTC day.
- A refused call never settles. A call refused as `busy` may still count against the day's cap.

## When something goes wrong

| error says | do this |
| --- | --- |
| the wallet's payment was turned down | run `wallet`; the balance is too low, tell your operator |
| the day's cap is reached | stop; tell your operator, or wait for the next UTC day |
| busy | every slot is taken; wait a few minutes, do not loop |
| no machine on sale | no host that runs it is listed; try later |
| the door does not know this lease | the leaseId is wrong, or the lease was not opened here |

Do not retry a paid command in a loop. Two failures in a row mean stop and report.

## What to tell your operator

- What it costs: each host sets its price, 0.007 USDC an hour today. A script run is 0.007. A home is about 0.17 a day, about 5 USDC
  for 30 days.
- What they do: send USDC on Base to the address `wallet` prints. Nothing else.
- What it is: live on Base mainnet since 2026-10-17. Hosts are run by independent operators, not vetted
  by Charter, and the host's operator can read a home's disk. No uptime figure. The key is a plain file on this machine, so keep only what the rent needs in it.

## More

- Every call and price: https://charterhome.dev/agents
- Machine-readable: https://charterhome.dev/llms.txt
- The same tools as an MCP server: `npx -y charter-mcp` (source, MIT: https://github.com/drew-dot-com/charter/tree/main/mcp)
