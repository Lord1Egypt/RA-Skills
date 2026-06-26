import { ethers } from 'ethers';
import { polyGasOverrides } from './gas.js';

const WMATIC  = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270';
const USDC_E  = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174';
const DEFAULT_QUOTER = '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6';
const DEFAULT_ROUTER = '0xE592427A0AEce92De3Edee1F18E0157C05861564';

// QuoterV1 ABI — individual params (not a struct like V2)
const QUOTER_ABI = [
  'function quoteExactOutputSingle(address tokenIn, address tokenOut, uint24 fee, uint256 amountOut, uint160 sqrtPriceLimitX96) returns (uint256 amountIn)',
];

// SwapRouter V1 ABI
// SwapRouter V1 does NOT auto-refund unspent native POL — refundETH() must be called explicitly.
// We use multicall to batch exactOutputSingle + refundETH in a single transaction.
const ROUTER_ABI = [
  'function exactOutputSingle(tuple(address tokenIn, address tokenOut, uint24 fee, address recipient, uint256 deadline, uint256 amountOut, uint256 amountInMaximum, uint160 sqrtPriceLimitX96) params) payable returns (uint256 amountIn)',
  'function refundETH() external payable',
  'function multicall(bytes[] calldata data) external payable returns (bytes[] memory results)',
];

// ERC-20 Transfer event for parsing receipt
const ERC20_TRANSFER_ABI = ['event Transfer(address indexed from, address indexed to, uint256 value)'];

/**
 * Get a quote for swapping POL → USDC.e using Uniswap V3 QuoterV1.
 * @param {{ usdceNeeded: number, provider: object, cfg: object }} params
 * @returns {{ polNeeded: BigNumber, rate: number }}
 */
export async function getSwapQuote({ usdceNeeded, provider, cfg }) {
  if (!Number.isFinite(usdceNeeded) || usdceNeeded <= 0) {
    throw new Error(`Invalid usdceNeeded: ${usdceNeeded}`);
  }
  const quoterAddr = cfg.yaml?.contracts?.uniswap_quoter ?? DEFAULT_QUOTER;
  if (!ethers.utils.isAddress(quoterAddr)) throw new Error(`Invalid contract address in config: uniswap_quoter = "${quoterAddr}"`);
  const quoter = new ethers.Contract(quoterAddr, QUOTER_ABI, provider);
  const amountOut = ethers.utils.parseUnits(usdceNeeded.toFixed(6), 6);

  let polNeeded;
  try {
    polNeeded = await quoter.callStatic.quoteExactOutputSingle(
      WMATIC,
      USDC_E,
      3000,
      amountOut,
      0,
    );
  } catch (e) {
    throw new Error(`Unable to get swap quote — check RPC or try again: ${e.message}`);
  }

  const rate = usdceNeeded / parseFloat(ethers.utils.formatEther(polNeeded));
  return { polNeeded, rate };
}

/**
 * Swap native POL → USDC.e using Uniswap V3 SwapRouter V1 exactOutputSingle.
 * @param {{ polAmountMax: BigNumber, usdceTarget: number, cfg: object, wallet: object, provider: object }} params
 * @returns {string} actual USDC.e received (formatted, e.g. "27.50")
 */
export async function swapPolToUsdc({ polAmountMax, usdceTarget, cfg, wallet, provider }) {
  if (!Number.isFinite(usdceTarget) || usdceTarget <= 0) {
    throw new Error(`Invalid usdceTarget: ${usdceTarget}`);
  }
  // Pre-flight: check POL balance
  const polBal = await provider.getBalance(wallet.address);
  if (polBal.lt(polAmountMax)) {
    throw new Error(
      `Insufficient POL: have ${ethers.utils.formatEther(polBal)} POL, need ${ethers.utils.formatEther(polAmountMax)} POL for swap`,
    );
  }

  const routerAddr = cfg.yaml?.contracts?.uniswap_router ?? DEFAULT_ROUTER;
  if (!ethers.utils.isAddress(routerAddr)) throw new Error(`Invalid contract address in config: uniswap_router = "${routerAddr}"`);
  const router = new ethers.Contract(routerAddr, ROUTER_ABI, provider);
  const routerSigned = router.connect(wallet);
  const routerIface = new ethers.utils.Interface(ROUTER_ABI);

  const deadline = Math.floor(Date.now() / 1000) + 600;
  const amountOut = ethers.utils.parseUnits(usdceTarget.toFixed(6), 6);

  // Batch exactOutputSingle + refundETH so unspent POL is returned in the same tx.
  // SwapRouter V1 does not auto-refund excess msg.value — explicit refundETH() is required.
  const swapCalldata   = routerIface.encodeFunctionData('exactOutputSingle', [{
    tokenIn:           WMATIC,
    tokenOut:          USDC_E,
    fee:               3000,
    recipient:         wallet.address,
    deadline,
    amountOut,
    amountInMaximum:   polAmountMax,
    sqrtPriceLimitX96: 0,
  }]);
  const refundCalldata = routerIface.encodeFunctionData('refundETH', []);

  const gasOverrides = await polyGasOverrides(provider);

  const tx = await routerSigned.multicall([swapCalldata, refundCalldata], {
    value: polAmountMax,
    ...gasOverrides,
  });
  console.log(`Swap tx submitted (${tx.hash?.slice(0, 12) ?? 'pending'}...), waiting for confirmation...`);
  const receipt = await tx.wait();

  // Parse actual USDC.e received from Transfer event (to=wallet)
  const iface = new ethers.utils.Interface(ERC20_TRANSFER_ABI);
  let received = amountOut; // fallback to target if log not found
  for (const log of receipt.logs) {
    if (log.address.toLowerCase() !== USDC_E.toLowerCase()) continue;
    try {
      const parsed = iface.parseLog(log);
      if (parsed.args.to.toLowerCase() === wallet.address.toLowerCase()) {
        received = parsed.args.value;
        break;
      }
    } catch { /* not a Transfer log */ }
  }

  return parseFloat(ethers.utils.formatUnits(received, 6)).toFixed(2);
}
