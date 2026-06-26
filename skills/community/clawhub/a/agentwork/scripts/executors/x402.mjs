import { randomBytes } from 'node:crypto';

export async function broadcastTx() {
  throw new Error('x402 executor does not broadcast raw EVM transactions');
}

function defaultFacilitatorId(executorType) {
  if (executorType === 'x402-okx') return 'okx_payments';
  return 'coinbase_cdp';
}

function encodeBase64Json(value) {
  return Buffer.from(JSON.stringify(value), 'utf8').toString('base64');
}

function decodeBase64Json(value) {
  return JSON.parse(Buffer.from(value, 'base64').toString('utf8'));
}

function createAuthorizationNonce() {
  return `0x${randomBytes(32).toString('hex')}`;
}

function requirePaymentRequirementExtraString(paymentRequirement, field, label) {
  const value = paymentRequirement.extra?.[field];
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new Error(`x402 payment requirement missing EIP-3009 ${label}`);
  }
  return value.trim();
}

async function signTransferWithAuthorization(wallet, paymentRequirement, walletAddress) {
  if (!wallet || typeof wallet.signTypedData !== 'function') {
    throw new Error('x402 executor requires a wallet with signTypedData()');
  }
  const address = walletAddress ?? wallet.address ?? wallet.account?.address;
  if (!address) {
    throw new Error('x402 executor could not resolve wallet address');
  }

  const chainId = Number(String(paymentRequirement.network ?? '').split(':')[1]);
  if (!Number.isFinite(chainId) || chainId <= 0) {
    throw new Error(`invalid x402 network: ${paymentRequirement.network ?? 'unknown'}`);
  }

  const tokenName = requirePaymentRequirementExtraString(paymentRequirement, 'name', 'token name');
  const tokenVersion = requirePaymentRequirementExtraString(paymentRequirement, 'version', 'token version');
  const now = Math.floor(Date.now() / 1000);
  const authorization = {
    from: address,
    to: paymentRequirement.payTo,
    value: String(paymentRequirement.amount),
    validAfter: String(now - 600),
    validBefore: String(now + Number(paymentRequirement.maxTimeoutSeconds ?? 300)),
    nonce: createAuthorizationNonce(),
  };
  const domain = {
    name: tokenName,
    version: tokenVersion,
    chainId,
    verifyingContract: paymentRequirement.asset,
  };
  const types = {
    TransferWithAuthorization: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' },
    ],
  };
  const message = {
    from: authorization.from,
    to: authorization.to,
    value: BigInt(authorization.value),
    validAfter: BigInt(authorization.validAfter),
    validBefore: BigInt(authorization.validBefore),
    nonce: authorization.nonce,
  };

  let signature;
  try {
    signature = await wallet.signTypedData(domain, types, message);
  } catch {
    signature = await wallet.signTypedData({
      domain,
      types,
      primaryType: 'TransferWithAuthorization',
      message,
    });
  }

  return {
    x402Version: 2,
    accepted: paymentRequirement,
    payload: {
      authorization,
      signature,
      chainIndex: chainId,
    },
  };
}

async function sendDepositRequest(url, body, apiKey, paymentSignature) {
  return await fetch(url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`,
      ...(paymentSignature ? { 'PAYMENT-SIGNATURE': paymentSignature } : {}),
    },
    body: JSON.stringify(body),
  });
}

export async function depositToEscrow(opts) {
  if (typeof globalThis.fetch !== 'function') {
    throw new Error('Node 18+ is required for x402 executor');
  }

  const baseUrl = opts.baseUrl ?? process.env.AGENTWORK_BASE_URL;
  const apiKey = opts.apiKey ?? process.env.AGENTWORK_API_KEY;
  if (!baseUrl || !apiKey) {
    throw new Error('AGENTWORK_BASE_URL and AGENTWORK_API_KEY are required for x402 executor');
  }

  const requestUrl = `${baseUrl.replace(/\/$/, '')}/agent/v1/orders/${opts.orderRef}/deposit`;
  const requestBody = {
    deposit_mode: 'x402',
    executor_type: opts.executorType ?? 'x402-cdp',
    facilitator_id: opts.facilitatorId ?? defaultFacilitatorId(opts.executorType),
  };

  let response = await sendDepositRequest(requestUrl, requestBody, apiKey, opts.paymentSignature);
  if (response.status === 402 && !opts.paymentSignature) {
    const paymentRequiredHeader = response.headers.get('PAYMENT-REQUIRED');
    if (!paymentRequiredHeader) {
      throw new Error('x402 deposit returned 402 without PAYMENT-REQUIRED header');
    }
    const paymentRequired = decodeBase64Json(paymentRequiredHeader);
    const paymentRequirement = Array.isArray(paymentRequired.accepts) ? paymentRequired.accepts[0] : null;
    if (!paymentRequirement) {
      throw new Error('x402 deposit returned invalid payment requirements');
    }

    const paymentPayload = await signTransferWithAuthorization(
      opts.wallet,
      paymentRequirement,
      opts.walletAddress,
    );
    if (paymentRequired.resource) {
      paymentPayload.resource = paymentRequired.resource;
    }
    response = await sendDepositRequest(
      requestUrl,
      requestBody,
      apiKey,
      encodeBase64Json(paymentPayload),
    );
  }

  const payload = await response.json().catch(() => null);
  if (response.status === 402) {
    return {
      payment_required: true,
      response: payload,
      headers: Object.fromEntries(response.headers.entries()),
    };
  }
  if (!response.ok) {
    throw new Error(`x402 deposit failed: ${JSON.stringify(payload)}`);
  }

  const paymentResponseHeader = response.headers.get('PAYMENT-RESPONSE');
  return {
    response: payload,
    payment_response: paymentResponseHeader ? decodeBase64Json(paymentResponseHeader) : null,
  };
}
