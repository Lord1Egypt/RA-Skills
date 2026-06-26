"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Web3Signer = void 0;
const ethers_1 = require("ethers");
const abi_1 = require("../contracts/abi");
const types_1 = require("../types/types");
const utils_1 = require("ethers/lib/utils");
const gasUtil_1 = require("../util/gasUtil");
const erc20Contract = new ethers_1.ethers.Contract(types_1.NULL_ADDRESS, abi_1.ContractABI.erc20.abi);
const erc721Contract = new ethers_1.ethers.Contract(types_1.NULL_ADDRESS, abi_1.ContractABI.erc721.abi);
const erc1155Contract = new ethers_1.ethers.Contract(types_1.NULL_ADDRESS, abi_1.ContractABI.erc1155.abi);
class Web3Signer {
    constructor(signer, chainId) {
        if (signer instanceof ethers_1.Signer) {
            if (!signer.provider) {
                throw Error('signer.provider is unset');
            }
        }
        this.signer = signer;
        this.chainId = chainId;
    }
    static getOrderHash(typedData) {
        return utils_1._TypedDataEncoder.hash(typedData.domain, typedData.types, typedData.message);
    }
    async signTypedData(account, typedData) {
        const signer = await this.getSigner(account);
        const typedDataSigner = signer;
        if (typedDataSigner._signTypedData) {
            const typeSignStr = await typedDataSigner._signTypedData(typedData.domain, typedData.types, typedData.message);
            const signer = ethers_1.ethers.utils.verifyTypedData(typedData.domain, typedData.types, typedData.message, typeSignStr);
            if (account.toLowerCase() !== signer.toLowerCase()) {
                throw Error(`signTypedData failed, account : ${account}, signer = ${signer}`);
            }
            return ethers_1.ethers.utils.splitSignature(typeSignStr);
        }
        else {
            throw Error('Unsupported signTypedData');
        }
    }
    async ethSend(call) {
        const transactionRequest = {
            from: call.from,
            to: call.to,
            data: call.data
        };
        if (call.value && ethers_1.ethers.BigNumber.from(call.value).gt(0)) {
            transactionRequest.value = ethers_1.ethers.BigNumber.from(call.value);
        }
        const signer = await this.getSigner(call.from);
        if (call.maxFeePerGas && call.maxPriorityFeePerGas) {
            transactionRequest.maxFeePerGas = ethers_1.ethers.BigNumber.from(call.maxFeePerGas);
            transactionRequest.maxPriorityFeePerGas = ethers_1.ethers.BigNumber.from(call.maxPriorityFeePerGas);
        }
        else if (call.gasPrice) {
            transactionRequest.gasPrice = ethers_1.ethers.BigNumber.from(call.gasPrice);
        }
        else {
            if (!(this.signer instanceof ethers_1.ethers.providers.Web3Provider)) {
                const gas = await (0, gasUtil_1.estimateGas)(this.chainId);
                if (gas) {
                    transactionRequest.maxFeePerGas = gas.maxFeePerGas;
                    transactionRequest.maxPriorityFeePerGas = gas.maxPriorityFeePerGas;
                }
            }
        }
        // Use provided gas limit if specified, otherwise let provider estimate
        if (call.gas) {
            transactionRequest.gasLimit = ethers_1.ethers.BigNumber.from(call.gas);
        }
        return await signer.sendTransaction(transactionRequest);
    }
    async getSigner(account) {
        let signer;
        if (this.signer instanceof ethers_1.ethers.providers.Web3Provider) {
            let accounts = await this.signer.listAccounts();
            if (!accounts?.length) {
                accounts = await this.signer.send('eth_requestAccounts', []);
                if (!accounts?.length) {
                    throw Error(`getSigner failed, accounts:${accounts}`);
                }
            }
            if (account) {
                if (!accounts.find(item => item.toString().toLowerCase() === account.toLowerCase())) {
                    throw Error(`Account mismatch, account:${account.toLowerCase()}, but connected accounts:${accounts}`);
                }
                signer = this.signer.getSigner(account);
            }
            else {
                signer = this.signer.getSigner(accounts[0]);
            }
            if (this.signer.provider?.isMetaMask && this.signer.provider?.request) {
                const chainId = await signer.getChainId();
                if (chainId != this.chainId) {
                    await this.signer.provider.request({
                        method: 'wallet_switchEthereumChain',
                        params: [{ chainId: '0x' + Number(this.chainId).toString(16) }]
                    });
                }
                else {
                    return signer;
                }
            }
        }
        else {
            signer = this.signer;
            const signerAddress = await signer.getAddress();
            if (account) {
                if (account.toLowerCase() !== signerAddress.toLowerCase()) {
                    throw Error(`Account mismatch, account: ${account.toLowerCase()}, but signer: ${signerAddress.toLowerCase()}`);
                }
            }
        }
        // const chainId = await signer.getChainId()
        // if (chainId != this.chainId) {
        //   throw Error(`chainId mismatch, chainId: ${ chainId }, but expected chainId: ${ this.chainId }`)
        // }
        return signer;
    }
    async getCurrentAccount() {
        let signer;
        if (this.signer instanceof ethers_1.ethers.providers.Web3Provider) {
            let accounts = await this.signer.listAccounts();
            if (accounts?.length) {
                return accounts[0].toLowerCase();
            }
            accounts = await this.signer.send('eth_requestAccounts', []);
            if (accounts?.length) {
                return accounts[0].toLowerCase();
            }
            throw Error('getCurrentAccount failed, please connect web3, and choose a account.');
        }
        else {
            signer = this.signer;
            const account = await signer.getAddress();
            return account.toLowerCase();
        }
    }
    async approveERC20Proxy(account, erc20Address, spender, gasParams, allowance) {
        const amount = allowance || ethers_1.ethers.constants.MaxInt256.toString();
        const transaction = await erc20Contract.populateTransaction.approve(spender, amount);
        if (transaction.data) {
            return this.ethSend({
                from: account,
                to: erc20Address,
                data: transaction.data,
                gasPrice: gasParams?.gasPrice,
                maxFeePerGas: gasParams?.maxFeePerGas,
                maxPriorityFeePerGas: gasParams?.maxPriorityFeePerGas
            });
        }
        throw Error(`approveERC20Proxy failed, account=${account}, erc20Address =${erc20Address}, spender=${spender}.`);
    }
    async approveERC721Proxy(account, erc721Address, operator, gasParams, approved = true) {
        const transaction = await erc721Contract.populateTransaction.setApprovalForAll(operator, approved);
        if (transaction.data) {
            return this.ethSend({
                from: account,
                to: erc721Address,
                data: transaction.data,
                gasPrice: gasParams?.gasPrice,
                maxFeePerGas: gasParams?.maxFeePerGas,
                maxPriorityFeePerGas: gasParams?.maxPriorityFeePerGas
            });
        }
        throw Error(`approveERC721Proxy failed, account=${account}, erc721Address =${erc721Address}, operator=${operator}.`);
    }
    async approveERC1155Proxy(account, erc1155Address, operator, gasParams, approved = true) {
        const transaction = await erc1155Contract.populateTransaction.setApprovalForAll(operator, approved);
        if (transaction.data) {
            return this.ethSend({
                from: account,
                to: erc1155Address,
                data: transaction.data,
                gasPrice: gasParams?.gasPrice,
                maxFeePerGas: gasParams?.maxFeePerGas,
                maxPriorityFeePerGas: gasParams?.maxPriorityFeePerGas
            });
        }
        throw Error(`approveERC1155Proxy failed, account=${account}, erc1155Address =${erc1155Address}, operator=${operator}.`);
    }
}
exports.Web3Signer = Web3Signer;
//# sourceMappingURL=Web3Signer.js.map