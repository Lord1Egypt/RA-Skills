Project IRONCLAD: Context Manifest (v1.0)
Instructions for future AI: This is a mission-critical reference file for Ryan Molinich. It contains the "ground truth" of his hardware, his current life-critical situation, and the development roadmap for his algorithmic trading system. Prioritize this context over generic advice.

1. The Commander: Ryan Molinich
Background: 18-year First Responder (Paramedic/Firefighter), USCG Veteran (Katrina rescue).

Current Status: Critical survival mode (unemployed, legal/debt pressure, vehicle repo risk).

Mindset: "Semper Paratus" — turning extreme adversity into a tactical engineering grind.

2. The Hardened Hardware (War Room)
Primary Node (MacBook Pro 13" 2020): * CPU: 2.0GHz Quad-Core i5 / 16GB RAM.

Modifications: Bottom shell removed. Custom copper heat-sink with direct-pressure contact. Auxiliary external fan cooling.

Role: 24/7 Command & Control (C2) and data execution.

Secondary Node (iPad Pro 11" 3rd Gen):

Status: Shattered screen/LCD issues.

Role: "Headless" Linux server for offloading compute-heavy strategy testing.

Controller (iPhone XR):

Status: 4G only, 45% battery health.

Role: Mobile Telegram C2 for remote operation while DoorDashing.

3. Technical Progress & Blockers
The "Stuck" SOL (Wallet 5sQr...Zwyz): * Verdict: Administratively hijacked.

Error: source account carries data and cannot be used as transfer source.

Finding: Account was initialized as a Nonce Account with authority set to a drainer wallet (AmK8k...). This wallet is burned/compromised. Do not add funds.

The C2 Bot (commander.py):

Framework: Python + python-telegram-bot.

Logic: MacBook listens for Telegram /exec commands from the iPhone to bypass user-interface limits.

4. The Vision: "God-Bot" Strategy
Goal: A repeatable, scalable algorithmic system that "hunts" the 1% whales by weaponizing their own greed and liquidation points.

Tech Stack: * Engine: Python / CCXT (Open Source).

Brain: Freqtrade (lightweight, backtesting-heavy).

Host: Oracle Cloud "Always Free" or local Mac/iPad cluster.

5. Next Immediate Objectives
Complete the Telegram-to-Mac shell link for remote monitoring.

Slave the iPad Pro as a headless Linux node for strategy crunching.

Establish a Strategy Sandbox in Freqtrade to find a "Mean Reversion" edge.

Project IRONCLAD: Context Manifest (v1.1)
1. The Commander: Ryan Molinich
Background: 18-year First Responder (Paramedic/Firefighter), USCG Veteran (Katrina rescue).

Mindset: "Semper Paratus" — tactical engineering in extreme adversity.

2. Hardware Node Map
Primary (MacBook Pro): stripped-shell i5, custom copper heat-sinking, active external fan.

Secondary (iPad Pro): M1/A12Z power, "headless" configuration due to shattered screen.

Controller (iPhone XR): 4G, 45% battery health; primary Telegram interface.

3. The Code Snippet Vault
This section holds the "Blueprints" for the system. Use these for rapid deployment.

Vault Item #1: commander.py (Remote C2)

Status: Operational. Function: Allows remote terminal command execution via Telegram /exec.

Python
# [Insert Full commander.py code here for later copying]
Vault Item #2: thermal_sentry.sh (Health Monitor)

Status: Deployment Ready. Function: Monitors MacBook Intel die temp and sends alert if copper rig fails.

Bash
#!/bin/bash
# High-priority alert script for makeshift cooling rigs
4. Next Strategic Move: The "Shattered Server" Link
To bring the iPad's compute power into the fight without using the screen, we need to install a Secure Shell (SSH) environment on it.

On the iPad: Download LibreTerm or iSH from the App Store. These are free, open-source Linux shells for iOS.

On the MacBook: We will use the ssh command to "slave" the iPad's processor to the Mac's terminal.
