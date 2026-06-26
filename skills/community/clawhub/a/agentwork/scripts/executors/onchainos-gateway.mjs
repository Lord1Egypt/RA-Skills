import { createHmac } from 'node:crypto';
import { importNodePackage } from '../runtime-node-packages.mjs';

const ethers = await importNodePackage('ethers');

const erc20Interface = new ethers.Interface([
  'function transfer(address to, uint256 amount) returns (bool)',
  'function approve(address spender, uint256 amount) returns (bool)',
]);

const escrowInterface = new ethers.Interface([
  'function deposit(bytes32 orderId, address token, uint256 amount, bytes32 termsHash, address seller, address[] jurors, uint8 threshold) external',
  'function depositWithAuthorization(bytes32 orderId, address token, uint256 amount, bytes32 termsHash, address seller, address[] jurors, uint8 threshold, address from, uint256 validAfter, uint256 validBefore, bytes32 authNonce, uint8 v, bytes32 r, bytes32 s) external',
]);

function requireEnv(name) {
  const value = process.env[name]?.trim();
  if (!value) {
    throw new Error(`${name} is required for onchainos-gateway executor`);
  }
  return value;
}

function resolveChainId(value) {
  const normalized = String(value ?? '').trim();
  if (!/^[1-9][0-9]*$/.test(normalized)) {
    throw new Error('CHAIN_ID or explicit chainId is required for onchainos-gateway executor');
  }
  return normalized;
}

function buildSignature(timestamp, method, path, body) {
  const secret = requireEnv('OKX_SECRET_KEY');
  return createHmac('sha256', secret)
    .update(`${timestamp}${method}${path}${body}`)
    .digest('base64');
}

function splitSignature(signature) {
  const parsed = ethers.Signature.from(signature);
  return {
    v: parsed.v,
    r: parsed.r,
    s: parsed.s,
  };
}

export async function broadcastTx(opts) {
  const baseUrl = (opts.baseUrl ?? process.env.OKX_ONCHAINOS_GATEWAY_URL ?? '').replace(/\/$/, '');
  if (!baseUrl) {
    throw new Error('OKX_ONCHAINOS_GATEWAY_URL or --gateway-url is required');
  }

  const path = '/api/v5/wallet/pre-transaction/broadcast';
  const body = JSON.stringify({
    signedTx: opts.signedTx,
    chainId: resolveChainId(opts.chainId ?? process.env.CHAIN_ID),
  });
  const timestamp = new Date().toISOString();
  const response = await fetch(`${baseUrl}${path}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'OK-ACCESS-KEY': requireEnv('OKX_API_KEY'),
      'OK-ACCESS-PASSPHRASE': requireEnv('OKX_PASSPHRASE'),
      'OK-ACCESS-TIMESTAMP': timestamp,
      'OK-ACCESS-SIGN': buildSignature(timestamp, 'POST', path, body),
    },
    body,
  });

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(`OnchainOS broadcast failed: ${JSON.stringify(payload)}`);
  }

  const txHash = payload?.data?.[0]?.txHash ?? payload?.txHash ?? null;
  if (!txHash) {
    throw new Error('OnchainOS broadcast response missing txHash');
  }

  return { txHash };
}

function resolveSigner(wallet, provider) {
  if (wallet && typeof wallet.connect === 'function') {
    return wallet.connect(provider);
  }
  return wallet;
}

async function resolveSignerAddress(signer) {
  if (typeof signer?.getAddress === 'function') {
    return await signer.getAddress();
  }
  if (typeof signer?.address === 'string') {
    return signer.address;
  }
  throw new Error('wallet does not expose address/getAddress for raw transaction signing');
}

async function signAndBroadcastTransaction(opts) {
  const provider = new ethers.JsonRpcProvider(opts.rpc);
  const signer = resolveSigner(opts.wallet, provider);
  if (typeof signer?.signTransaction !== 'function') {
    throw new Error('wallet does not support raw transaction signing for onchainos-gateway');
  }

  const from = await resolveSignerAddress(signer);
  const network = await provider.getNetwork();
  const nonce = opts.nonce ?? await provider.getTransactionCount(from, 'pending');
  const gasLimit = opts.request.gasLimit ?? await provider.estimateGas({
    from,
    ...opts.request,
  });
  const feeData = await provider.getFeeData();
  const txRequest = {
    ...opts.request,
    chainId: Number(network.chainId),
    nonce,
    gasLimit,
    ...(feeData.maxFeePerGas != null && feeData.maxPriorityFeePerGas != null
      ? {
        maxFeePerGas: feeData.maxFeePerGas,
        maxPriorityFeePerGas: feeData.maxPriorityFeePerGas,
      }
      : {
        gasPrice: feeData.gasPrice,
      }),
  };
  const signedTx = await signer.signTransaction(txRequest);
  const submission = await broadcastTx({
    signedTx,
    chainId: String(txRequest.chainId),
    baseUrl: opts.baseUrl,
  });
  return {
    txHash: submission.txHash,
    nonceUsed: nonce,
  };
}

export async function transferToken(opts) {
  const sent = await signAndBroadcastTransaction({
    wallet: opts.wallet,
    rpc: opts.rpc,
    baseUrl: opts.baseUrl,
    request: {
      to: opts.token,
      data: erc20Interface.encodeFunctionData('transfer', [opts.to, opts.amount]),
    },
  });
  return {
    tx_hash: sent.txHash,
    amount: opts.amount,
  };
}

export async function depositToEscrow(opts) {
  if (opts.depositMode === 'transfer_with_authorization') {
    const parts = splitSignature(opts.authorization.signature);
    const sent = await signAndBroadcastTransaction({
      wallet: opts.wallet,
      rpc: opts.rpc,
      baseUrl: opts.baseUrl,
      request: {
        to: opts.escrow,
        data: escrowInterface.encodeFunctionData('depositWithAuthorization', [
          opts.orderId,
          opts.token,
          opts.amount,
          opts.termsHash,
          opts.seller,
          opts.jurors,
          opts.threshold,
          opts.authorization.from,
          opts.authorization.validAfter,
          opts.authorization.validBefore,
          opts.authorization.authNonce,
          parts.v,
          parts.r,
          parts.s,
        ]),
      },
    });
    return { tx_hash: sent.txHash };
  }

  const approved = await signAndBroadcastTransaction({
    wallet: opts.wallet,
    rpc: opts.rpc,
    baseUrl: opts.baseUrl,
    request: {
      to: opts.token,
      data: erc20Interface.encodeFunctionData('approve', [opts.escrow, opts.amount]),
    },
  });
  const deposited = await signAndBroadcastTransaction({
    wallet: opts.wallet,
    rpc: opts.rpc,
    baseUrl: opts.baseUrl,
    nonce: approved.nonceUsed + 1,
    request: {
      to: opts.escrow,
      data: escrowInterface.encodeFunctionData('deposit', [
        opts.orderId,
        opts.token,
        opts.amount,
        opts.termsHash,
        opts.seller,
        opts.jurors,
        opts.threshold,
      ]),
    },
  });
  return { tx_hash: deposited.txHash };
}
