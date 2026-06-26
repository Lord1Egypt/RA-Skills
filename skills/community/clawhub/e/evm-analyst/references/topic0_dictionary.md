# Topic0 字典

skill 在解码 log 时优先查本字典，未命中再调 OpenChain Signature Database API
(https://api.openchain.xyz/signature-database/v1/lookup)。

字段：`topic0_hash` -> `event_signature` -> `protocol_family`

---

## ERC 标准

| topic0 | signature | family |
|---|---|---|
| `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef` | Transfer(address,address,uint256) | ERC20 / ERC721 |
| `0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925` | Approval(address,address,uint256) | ERC20 / ERC721 |
| `0x17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31` | ApprovalForAll(address,address,bool) | ERC721 / ERC1155 |
| `0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62` | TransferSingle | ERC1155 |
| `0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb` | TransferBatch | ERC1155 |

## Uniswap V2 / QuickSwap V2

| topic0 | signature | family |
|---|---|---|
| `0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822` | Swap(address,uint256,uint256,uint256,uint256,address) | V2 Pair |
| `0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1` | Sync(uint112,uint112) | V2 Pair |
| `0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f` | Mint(address,uint256,uint256) | V2 Pair |
| `0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496` | Burn(address,uint256,uint256,address) | V2 Pair |

## Uniswap V3 / QuickSwap V3

| topic0 | signature | family |
|---|---|---|
| `0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67` | Swap | V3 Pool |
| `0x7a53080ba414158be7ec69b987b5fb7d07dee101fe85488f0853ae16239d0bde` | Mint | V3 Pool |
| `0x0c396cd989a39f4459b5fa1aed6a9a8dcdbc45908acfd67e028cd568da98982c` | Burn | V3 Pool |

## WETH / Vault

| topic0 | signature | family |
|---|---|---|
| `0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c` | Deposit(address,uint256) | WETH / Vault |
| `0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65` | Withdrawal(address,uint256) | WETH / Vault |

## OHM-fork / Origin (LGNS) 风格

注：以下签名需要根据 Origin 实际合约 ABI 在 Polygonscan 确认。计算方法：
`keccak256("EventName(type1,type2,...)")` = topic0

| topic0 | signature | family | 备注 |
|---|---|---|---|
| `0x9e71bc8eea02a63969f509818f2dafb9254532904319f9dbda79b67bd34a5f3d` | Staked(address,uint256) | OHM-fork staking | Staking.Staked(user, amount), topic1=用户地址 |
| `0x405b10f0bd071c3c7407d252cea4f522291a502e06f69b37b6af994a59f330a8` | Transfer(gons) | sLGNS配对Transfer | sLGNS.Transfer配对gons记账，topic1=from, topic2=to |
| `0x917acfbe39be6509ccf7fecb66a7e42ce2be1083c2d7dd3b9b7491dabddb8da4` | EpochBegin(uint256,uint256) | OHM-fork rebase | sLGNS.EpochBegin(epoch, timestamp), topic1=epoch号 |
| `0x6012dbce857565c4a40974aa5de8373a761fc429077ef0c8c8611d1e20d63fb2` | RebaseAmount(uint256,uint256) | OHM-fork rebase | sLGNS.RebaseAmount(epoch, amount), topic1=epoch号 |
| `0xfa8ccab40e7da8146c2304cd0950334fd30a6ba093abe86261aa13911fed849c` | Distributed(address,address,uint256) | Treasury分发 | Treasury.分发记录(distributor, staking, amount), topic1=StakingDistributor |

**确认实际签名的方法**：
1. 拿 sample_tx 在 Polygonscan 打开 Logs
2. 找 contract_address = LGNS / Staking / Bond 的 log 行
3. Polygonscan 自动解码后会显示事件名
4. 把事件签名字符串扔进 keccak256 计算器即得 topic0

---

## 扩展方法

新增条目时直接编辑本文件。如需批量添加某协议的事件，从 Etherscan / Polygonscan 拉合约 ABI，对每个 event 计算 keccak256(signature)。
