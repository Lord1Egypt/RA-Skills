import { Web3Signer } from '../signer/Web3Signer'
import { BigNumber, Contract } from 'ethers'
import { ContractABI, CONTRACTS_ADDRESSES } from '../contracts/config'
import { GasParams } from '../types/types'

export async function erc20Decimals(web3Signer: Web3Signer, tokenAddress: string) {
  const signer = await web3Signer.getSigner()
  const contract = new Contract(tokenAddress, ContractABI.erc20.abi, signer)
  return await contract.decimals()
}

export async function approveERC20(
  web3Signer: Web3Signer,
  tokenAddress: string,
  value: BigNumber,
  gasParams?: GasParams
) {
  if (value.eq(0)) {
    return
  }
  
  const chainId = web3Signer.chainId
  const signer = await web3Signer.getSigner()
  const owner = await signer.getAddress()
  const elementEx = CONTRACTS_ADDRESSES[chainId].ElementEx
  
  const contract = new Contract(tokenAddress, ContractABI.erc20.abi, signer)
  const allowance = await contract.allowance(owner, elementEx)
  if (allowance.lt(value)) {
    const tx = await web3Signer.approveERC20Proxy(owner, tokenAddress, elementEx, gasParams)
    await tx.wait()
  }
}

export async function setApproveForAll(
  web3Signer: Web3Signer,
  tokenAddress: string,
  gasParams?: GasParams
) {
  const chainId = web3Signer.chainId
  const signer = await web3Signer.getSigner()
  const owner = await signer.getAddress()
  const elementEx = CONTRACTS_ADDRESSES[chainId].ElementEx

  const contract = new Contract(tokenAddress, ContractABI.erc721.abi, signer)
  const approved = await contract.isApprovedForAll(owner, elementEx)
  if (!approved) {
    const tx = await web3Signer.approveERC721Proxy(owner, tokenAddress, elementEx, gasParams)
    await tx.wait()
  }
}

export async function transferERC721(
  web3Signer: Web3Signer,
  tokenAddress: string,
  tokenId: string,
  toAddress: string,
  gasParams?: GasParams
) {
  const signer = await web3Signer.getSigner()
  const contract = new Contract(tokenAddress, ContractABI.erc721.abi, signer)
  const fromAddress = await signer.getAddress()

  // Check if contract supports safeTransferFrom
  const safeTransferFragment = contract.interface.getFunction('safeTransferFrom')
  if (!safeTransferFragment) {
    throw new Error('Contract does not support safeTransferFrom')
  }

  // Use safeTransferFrom(address from, address to, uint256 tokenId)
  const tx = await contract.safeTransferFrom(fromAddress, toAddress, tokenId, gasParams || {})
  return await tx.wait()
}

export async function transferERC1155(
  web3Signer: Web3Signer,
  tokenAddress: string,
  tokenId: string,
  toAddress: string,
  quantity: string,
  gasParams?: GasParams
) {
  const signer = await web3Signer.getSigner()
  const fromAddress = await signer.getAddress()

  // Check if contract supports safeTransferFrom
  const contract = new Contract(tokenAddress, ContractABI.erc1155.abi, signer)

  const safeTransferFragment = contract.interface.getFunction('safeTransferFrom')
  if (!safeTransferFragment) {
    throw new Error('Contract does not support safeTransferFrom')
  }

  // Use safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes data)
  const tx = await contract.safeTransferFrom(fromAddress, toAddress, tokenId, quantity, '0x', gasParams || {})
  return await tx.wait()
}

