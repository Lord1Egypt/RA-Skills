# Blockchain Web3 Toolkit

## 简介 / Introduction

一站式区块链开发工具包，为开发者和用户提供便捷的以太坊生态系统交互能力。

An all-in-one blockchain development toolkit providing convenient interaction with the Ethereum ecosystem for developers and users.

## 功能特性 / Features

- **钱包管理 / Wallet Management**: 创建、导入、备份以太坊钱包
- **合约交互 / Contract Interaction**: 部署和调用智能合约
- **NFT操作 / NFT Operations**: 铸造、转移、查询NFT
- **Gas监控 / Gas Monitoring**: 实时追踪网络Gas价格
- **代币工具 / Token Tools**: ERC20代币余额查询与转账

## 安装 / Installation

```bash
pip install -r requirements.txt
```

## 快速开始 / Quick Start

```python
from scripts.wallet_manager import WalletManager

# 创建新钱包
wallet = WalletManager.create_wallet()
print(f"Address: {wallet.address}")
print(f"Private Key: {wallet.private_key}")

# 查询余额
balance = WalletManager.get_balance("0x...")
print(f"Balance: {balance} ETH")
```

## 配置 / Configuration

在 `.env` 文件中设置以下环境变量：

```
INFURA_API_KEY=your_infura_key
ETHERSCAN_API_KEY=your_etherscan_key
DEFAULT_NETWORK=mainnet
```

## API文档 / API Documentation

### WalletManager

```python
class WalletManager:
    @staticmethod
    def create_wallet() -> Wallet
    @staticmethod
    def import_from_private_key(private_key: str) -> Wallet
    @staticmethod
    def get_balance(address: str, network: str = "mainnet") -> float
```

### ContractInterface

```python
class ContractInterface:
    def deploy(self, abi: dict, bytecode: str, *args) -> str
    def call(self, contract_address: str, function_name: str, *args)
    def send_transaction(self, contract_address: str, function_name: str, *args) -> str
```

## 安全提示 / Security Notes

⚠️ **警告**: 永远不要将私钥提交到版本控制或分享给他人！

⚠️ **Warning**: Never commit private keys to version control or share them with others!

## 许可证 / License

MIT License
