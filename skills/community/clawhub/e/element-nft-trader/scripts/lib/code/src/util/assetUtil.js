"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.erc20Decimals = erc20Decimals;
exports.approveERC20 = approveERC20;
exports.setApproveForAll = setApproveForAll;
exports.transferERC721 = transferERC721;
exports.transferERC1155 = transferERC1155;
const ethers_1 = require("ethers");
const config_1 = require("../contracts/config");
async function erc20Decimals(web3Signer, tokenAddress) {
    const signer = await web3Signer.getSigner();
    const contract = new ethers_1.Contract(tokenAddress, config_1.ContractABI.erc20.abi, signer);
    return await contract.decimals();
}
async function approveERC20(web3Signer, tokenAddress, value, gasParams) {
    if (value.eq(0)) {
        return;
    }
    const chainId = web3Signer.chainId;
    const signer = await web3Signer.getSigner();
    const owner = await signer.getAddress();
    const elementEx = config_1.CONTRACTS_ADDRESSES[chainId].ElementEx;
    const contract = new ethers_1.Contract(tokenAddress, config_1.ContractABI.erc20.abi, signer);
    const allowance = await contract.allowance(owner, elementEx);
    if (allowance.lt(value)) {
        const tx = await web3Signer.approveERC20Proxy(owner, tokenAddress, elementEx, gasParams);
        await tx.wait();
    }
}
async function setApproveForAll(web3Signer, tokenAddress, gasParams) {
    const chainId = web3Signer.chainId;
    const signer = await web3Signer.getSigner();
    const owner = await signer.getAddress();
    const elementEx = config_1.CONTRACTS_ADDRESSES[chainId].ElementEx;
    const contract = new ethers_1.Contract(tokenAddress, config_1.ContractABI.erc721.abi, signer);
    const approved = await contract.isApprovedForAll(owner, elementEx);
    if (!approved) {
        const tx = await web3Signer.approveERC721Proxy(owner, tokenAddress, elementEx, gasParams);
        await tx.wait();
    }
}
async function transferERC721(web3Signer, tokenAddress, tokenId, toAddress, gasParams) {
    const signer = await web3Signer.getSigner();
    const contract = new ethers_1.Contract(tokenAddress, config_1.ContractABI.erc721.abi, signer);
    const fromAddress = await signer.getAddress();
    // Check if contract supports safeTransferFrom
    const safeTransferFragment = contract.interface.getFunction('safeTransferFrom');
    if (!safeTransferFragment) {
        throw new Error('Contract does not support safeTransferFrom');
    }
    // Use safeTransferFrom(address from, address to, uint256 tokenId)
    const tx = await contract.safeTransferFrom(fromAddress, toAddress, tokenId, gasParams || {});
    return await tx.wait();
}
async function transferERC1155(web3Signer, tokenAddress, tokenId, toAddress, quantity, gasParams) {
    const signer = await web3Signer.getSigner();
    const fromAddress = await signer.getAddress();
    // Check if contract supports safeTransferFrom
    const contract = new ethers_1.Contract(tokenAddress, config_1.ContractABI.erc1155.abi, signer);
    const safeTransferFragment = contract.interface.getFunction('safeTransferFrom');
    if (!safeTransferFragment) {
        throw new Error('Contract does not support safeTransferFrom');
    }
    // Use safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes data)
    const tx = await contract.safeTransferFrom(fromAddress, toAddress, tokenId, quantity, '0x', gasParams || {});
    return await tx.wait();
}
//# sourceMappingURL=assetUtil.js.map