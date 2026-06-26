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

export async function getBalances(opts) {
  const provider = new ethers.JsonRpcProvider(opts.rpc);
  const erc20 = new ethers.Contract(
    opts.token,
    [
      'function balanceOf(address) view returns (uint256)',
      'function symbol() view returns (string)',
      'function decimals() view returns (uint8)',
    ],
    provider,
  );

  const [ethBalance, tokenBalance, symbol, decimals] = await Promise.all([
    provider.getBalance(opts.address),
    erc20.balanceOf(opts.address),
    erc20.symbol().catch(() => 'UNKNOWN'),
    erc20.decimals().catch(() => 6),
  ]);

  return {
    token_balance: tokenBalance.toString(),
    native_balance: ethBalance.toString(),
    eth_balance: ethBalance.toString(),
    token_symbol: symbol,
    token_decimals: Number(decimals),
  };
}

export async function broadcastTx(opts) {
  if (typeof opts.send !== 'function') {
    throw new Error('broadcastTx requires send() callback');
  }
  const tx = await opts.send();
  const receipt = await tx.wait();
  return {
    txHash: receipt.hash,
  };
}

function resolveTransactor(wallet, provider) {
  if (wallet && typeof wallet.connect === 'function') {
    return wallet.connect(provider);
  }
  return wallet;
}

async function waitForTransactionHash(provider, txResult) {
  const txHash = typeof txResult === 'string'
    ? txResult
    : (txResult?.hash ?? txResult?.txHash ?? txResult?.transactionHash ?? null);
  if (!txHash) {
    throw new Error('transaction result missing hash');
  }

  if (typeof txResult?.wait === 'function') {
    const receipt = await txResult.wait();
    return receipt?.hash ?? receipt?.transactionHash ?? txHash;
  }

  const receipt = await provider.waitForTransaction(txHash);
  return receipt?.hash ?? receipt?.transactionHash ?? txHash;
}

async function sendTransactionWithWallet(opts) {
  const transactor = resolveTransactor(opts.wallet, opts.provider);
  if (typeof transactor?.sendTransaction !== 'function') {
    throw new Error('wallet does not support sendTransaction');
  }
  const txResult = await transactor.sendTransaction(opts.request);
  return await waitForTransactionHash(opts.provider, txResult);
}

export async function transferToken(opts) {
  const provider = new ethers.JsonRpcProvider(opts.rpc);
  const txHash = await sendTransactionWithWallet({
    wallet: opts.wallet,
    provider,
    request: {
      to: opts.token,
      data: erc20Interface.encodeFunctionData('transfer', [opts.to, opts.amount]),
    },
  });
  return {
    tx_hash: txHash,
    amount: opts.amount,
  };
}

function splitSignature(signature) {
  const parsed = ethers.Signature.from(signature);
  return {
    v: parsed.v,
    r: parsed.r,
    s: parsed.s,
  };
}

export async function depositToEscrow(opts) {
  const depositMode = opts.depositMode ?? 'approve_deposit';
  if (depositMode !== 'approve_deposit' && depositMode !== 'transfer_with_authorization') {
    throw new Error(
      `local-rpc executor does not support deposit mode ${depositMode}; use approve_deposit or transfer_with_authorization`,
    );
  }
  const provider = new ethers.JsonRpcProvider(opts.rpc);

  if (depositMode === 'transfer_with_authorization') {
    const parts = splitSignature(opts.authorization.signature);
    const txHash = await sendTransactionWithWallet({
      wallet: opts.wallet,
      provider,
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
    return { tx_hash: txHash };
  }

  await sendTransactionWithWallet({
    wallet: opts.wallet,
    provider,
    request: {
      to: opts.token,
      data: erc20Interface.encodeFunctionData('approve', [opts.escrow, opts.amount]),
    },
  });

  const txHash = await sendTransactionWithWallet({
    wallet: opts.wallet,
    provider,
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
  return { tx_hash: txHash };
}
