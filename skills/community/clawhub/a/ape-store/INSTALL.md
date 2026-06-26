# Ape.Store Token Creator - OpenClaw Skill

## Requirements
- Node.js installed
- OpenClaw 2026.2.14 or later

## Installation

1. Copy the skill folder to your computer

2. Open a terminal inside the skill folder and run:
   npm install

3. Open skill.json and update your config:
   - privateKey: your wallet private key
   - rpcUrl: your BASE RPC URL (default is https://mainnet.base.org)

## Usage

Trigger the skill from OpenClaw with:

   create a token on ape.store with the name MyToken and the symbol MTK and the description My token description

With optional image:

   create a token on ape.store with the name MyToken and the symbol MTK and the description My token description and image C:\path\to\image.png

## Notes
- Wallet must have ETH on BASE network to cover gas fees
- Image formats supported: jpg, png, gif, webp