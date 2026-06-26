import { ContractABI, CONTRACTS_ADDRESSES } from './config'
import { Contract, Signer } from 'ethers'

export { ContractABI } from './abi/index'

export function getElementExContract(chainId: number, signer: Signer): Contract {
  const address = CONTRACTS_ADDRESSES[chainId as keyof typeof CONTRACTS_ADDRESSES].ElementEx
  return new Contract(address, ContractABI.elementEx.abi, signer)
}

// export function getElementExSwapContract(chainId: number, signer: Signer): Contract {
//   const address = CONTRACTS_ADDRESSES[chainId as keyof typeof CONTRACTS_ADDRESSES].ElementExSwapV2
//   return new Contract(address, ContractABI.elementExSwap.abi, signer)
// }

export function getHelperContract(chainId: number, signer: Signer): Contract {
  const address = CONTRACTS_ADDRESSES[chainId as keyof typeof CONTRACTS_ADDRESSES].Helper
  return new Contract(address, ContractABI.helper.abi, signer)
}
