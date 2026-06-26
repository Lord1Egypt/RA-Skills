import { FxSdk, tokens } from '@aladdindao/fx-sdk'
import type { Address } from 'viem'

/** Token key for fxSAVE deposit/withdraw */
export type FxSaveTokenKey = 'usdc' | 'fxUSD' | 'fxUSDBasePool'

export type FxAction =
  | {
      kind: 'getPositions'
      userAddress: Address
      market: 'ETH' | 'BTC'
      type: 'long' | 'short'
    }
  | {
      kind: 'increasePosition'
      market: 'ETH' | 'BTC'
      type: 'long' | 'short'
      positionId: number
      leverage: number
      inputTokenAddress: Address
      amount: bigint
      slippage: number
      userAddress: Address
    }
  | {
      kind: 'reducePosition'
      market: 'ETH' | 'BTC'
      type: 'long' | 'short'
      positionId: number
      outputTokenAddress: Address
      amount: bigint
      slippage: number
      userAddress: Address
      isClosePosition?: boolean
    }
  | {
      kind: 'adjustPositionLeverage'
      market: 'ETH' | 'BTC'
      type: 'long' | 'short'
      positionId: number
      leverage: number
      slippage: number
      userAddress: Address
    }
  | {
      kind: 'getBridgeQuote'
      sourceChainId: 1 | 8453
      destChainId: 1 | 8453
      token: string
      amount: bigint
      recipient: Address
      sourceRpcUrl?: string
    }
  | {
      kind: 'buildBridgeTx'
      sourceChainId: 1 | 8453
      destChainId: 1 | 8453
      token: string
      amount: bigint
      recipient: Address
      refundAddress?: Address
      sourceRpcUrl?: string
    }
  | { kind: 'getFxSaveBalance'; userAddress: Address }
  | { kind: 'getFxSaveRedeemStatus'; userAddress: Address }
  | { kind: 'getFxSaveClaimable'; userAddress: Address }
  | { kind: 'getRedeemTx'; userAddress: Address; receiver?: Address }
  | {
      kind: 'depositFxSave'
      userAddress: Address
      tokenIn: FxSaveTokenKey
      amount: bigint
      slippage?: number
    }
  | {
      kind: 'withdrawFxSave'
      userAddress: Address
      tokenOut: FxSaveTokenKey
      amount: bigint
      instant?: boolean
      slippage?: number
    }

export interface AdapterOptions {
  rpcUrl?: string
  chainId?: number
  planOnly?: boolean
}

export async function runFxAction(action: FxAction, options: AdapterOptions = {}) {
  const chainId = options.chainId ?? 1
  const sdk = new FxSdk({ rpcUrl: options.rpcUrl, chainId })

  if (action.kind === 'getPositions') {
    return sdk.getPositions(action)
  }

  if (action.kind === 'increasePosition') {
    const result = await sdk.increasePosition(action)
    if (options.planOnly ?? true) {
      return { mode: 'plan' as const, positionId: result.positionId, routes: result.routes }
    }
    return {
      mode: 'execute_required' as const,
      message: 'Use wallet client to send selected route.txs sequentially.',
      routePreview: result.routes[0],
    }
  }

  if (action.kind === 'reducePosition') {
    const result = await sdk.reducePosition(action)
    if (options.planOnly ?? true) {
      return { mode: 'plan' as const, positionId: result.positionId, routes: result.routes }
    }
    return {
      mode: 'execute_required' as const,
      message: 'Use wallet client to send selected route.txs sequentially.',
      routePreview: result.routes[0],
    }
  }

  if (action.kind === 'adjustPositionLeverage') {
    const result = await sdk.adjustPositionLeverage(action)
    if (options.planOnly ?? true) {
      return { mode: 'plan' as const, positionId: result.positionId, routes: result.routes }
    }
    return {
      mode: 'execute_required' as const,
      message: 'Use wallet client to send selected route.txs sequentially.',
      routePreview: result.routes[0],
    }
  }

  if (action.kind === 'getBridgeQuote') {
    const quote = await sdk.getBridgeQuote({
      sourceChainId: action.sourceChainId,
      destChainId: action.destChainId,
      token: action.token,
      amount: action.amount,
      recipient: action.recipient,
      sourceRpcUrl: action.sourceRpcUrl,
    })
    return { mode: 'plan' as const, quote }
  }

  if (action.kind === 'buildBridgeTx') {
    const result = await sdk.buildBridgeTx({
      sourceChainId: action.sourceChainId,
      destChainId: action.destChainId,
      token: action.token,
      amount: action.amount,
      recipient: action.recipient,
      refundAddress: action.refundAddress,
      sourceRpcUrl: action.sourceRpcUrl,
    })
    if (options.planOnly ?? true) {
      return { mode: 'plan' as const, tx: result.tx, quote: result.quote }
    }
    return {
      mode: 'execute_required' as const,
      message: 'Use wallet client to send result.tx (to, data, value) on source chain.',
      tx: result.tx,
      quote: result.quote,
    }
  }

  if (action.kind === 'getFxSaveBalance') {
    return sdk.getFxSaveBalance({ userAddress: action.userAddress })
  }

  if (action.kind === 'getFxSaveRedeemStatus') {
    return sdk.getFxSaveRedeemStatus({ userAddress: action.userAddress })
  }

  if (action.kind === 'getFxSaveClaimable') {
    return sdk.getFxSaveClaimable({ userAddress: action.userAddress })
  }

  if (action.kind === 'getRedeemTx') {
    const result = await sdk.getRedeemTx({
      userAddress: action.userAddress,
      receiver: action.receiver,
    })
    if (options.planOnly ?? true) {
      return { mode: 'plan' as const, txs: result.txs }
    }
    return {
      mode: 'execute_required' as const,
      message: 'Use wallet client to send result.txs in order (claim after cooldown).',
      txs: result.txs,
    }
  }

  if (action.kind === 'depositFxSave') {
    const result = await sdk.depositFxSave({
      userAddress: action.userAddress,
      tokenIn: action.tokenIn,
      amount: action.amount,
      slippage: action.slippage,
    })
    if (options.planOnly ?? true) {
      return { mode: 'plan' as const, txs: result.txs }
    }
    return {
      mode: 'execute_required' as const,
      message: 'Use wallet client to send result.txs in order (approve then deposit).',
      txs: result.txs,
    }
  }

  if (action.kind === 'withdrawFxSave') {
    const result = await sdk.withdrawFxSave({
      userAddress: action.userAddress,
      tokenOut: action.tokenOut,
      amount: action.amount,
      instant: action.instant,
      slippage: action.slippage,
    })
    if (options.planOnly ?? true) {
      return { mode: 'plan' as const, txs: result.txs }
    }
    return {
      mode: 'execute_required' as const,
      message: 'Use wallet client to send result.txs in order.',
      txs: result.txs,
    }
  }

  throw new Error('Unsupported action kind')
}

// Example payloads for agent planners
export const sampleIncreasePayload: FxAction = {
  kind: 'increasePosition',
  market: 'ETH',
  type: 'short',
  positionId: 0,
  leverage: 3,
  inputTokenAddress: tokens.wstETH as Address,
  amount: 10n ** 17n,
  slippage: 1,
  userAddress: '0x0000000000000000000000000000000000000001',
}

export const sampleDepositFxSavePayload: FxAction = {
  kind: 'depositFxSave',
  userAddress: '0x0000000000000000000000000000000000000001',
  tokenIn: 'usdc',
  amount: 1_000_000n, // 1 USDC (6 decimals)
  slippage: 0.5,
}
