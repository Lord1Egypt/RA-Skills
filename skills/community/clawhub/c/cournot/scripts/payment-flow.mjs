function fail(message) {
  throw new Error(message);
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function sameValue(left, right) {
  const a = String(left);
  const b = String(right);
  if (/^0x[0-9a-f]+$/i.test(a) && /^0x[0-9a-f]+$/i.test(b)) {
    return a.toLowerCase() === b.toLowerCase();
  }
  return a === b;
}

function decodeBase64Json(value, label) {
  if (typeof value !== "string" || value.trim() === "") {
    fail(`${label} must be a non-empty base64 string`);
  }

  const normalized = value.replaceAll(/\s/g, "");
  if (!/^[A-Za-z0-9+/]*={0,2}$/.test(normalized)) {
    fail(`${label} is not valid base64`);
  }

  try {
    return JSON.parse(Buffer.from(normalized, "base64").toString("utf8"));
  } catch {
    fail(`${label} does not contain valid JSON`);
  }
}

export function parsePaymentRequirements(input) {
  const requirements =
    typeof input === "string"
      ? decodeBase64Json(input, "PAYMENT-REQUIRED")
      : structuredClone(input);

  if (!isObject(requirements)) fail("Payment requirements must be an object");
  if (requirements.x402Version == null) {
    fail("Payment requirements are missing x402Version");
  }
  if (!Array.isArray(requirements.accepts) || requirements.accepts.length === 0) {
    fail("Payment requirements must contain at least one accepts entry");
  }

  requirements.accepts.forEach((accept, acceptIndex) => {
    if (!isObject(accept)) fail(`accepts[${acceptIndex}] must be an object`);
    for (const field of ["scheme", "network", "asset", "amount", "payTo"]) {
      if (accept[field] == null || String(accept[field]) === "") {
        fail(`accepts[${acceptIndex}] is missing ${field}`);
      }
    }
  });

  return requirements;
}

export function enumeratePaymentOptions(input) {
  const requirements = parsePaymentRequirements(input);
  return requirements.accepts.map((accept, acceptIndex) => ({
    index: acceptIndex + 1,
    acceptIndex,
    ...structuredClone(accept),
  }));
}

function supportsValue(supported, actual) {
  if (supported == null || supported === "*") return true;
  const values = Array.isArray(supported) ? supported : [supported];
  return values.some((value) => value === "*" || sameValue(value, actual));
}

export function walletSupportsOption(wallet, option) {
  if (!isObject(wallet) || wallet.available === false) return false;
  return (
    supportsValue(wallet.networks, option.network) &&
    supportsValue(wallet.schemes, option.scheme) &&
    supportsValue(wallet.assets, option.asset) &&
    supportsValue(wallet.transferMethods, option.extra?.assetTransferMethod)
  );
}

export function planPayment(input, wallets = []) {
  const requirements = parsePaymentRequirements(input);
  if (!Array.isArray(wallets)) fail("wallets must be an array");

  const options = enumeratePaymentOptions(requirements).map((option) => ({
    ...option,
    compatibleWallets: wallets
      .filter((wallet) => walletSupportsOption(wallet, option))
      .map((wallet) => ({ id: wallet.id, name: wallet.name || wallet.id })),
  }));
  const compatibleOptions = options.filter(
    (option) => option.compatibleWallets.length > 0
  );
  const bscOptions = options.filter((option) => option.network === "eip155:56");

  let state;
  if (wallets.length === 0) state = "wallet_required";
  else if (compatibleOptions.length === 0) state = "no_compatible_wallet";
  else if (compatibleOptions.length === 1) state = "confirmation_required";
  else state = "selection_required";

  const setupRecommendations = [
    {
      id: "x402-foundation",
      label: "x402 Foundation Buyer SDK",
      appliesToOptionIndexes: options.map((option) => option.index),
    },
    {
      id: "viem-local-account",
      label: "viem Local Account signer",
      appliesToOptionIndexes: options.map((option) => option.index),
    },
  ];

  if (wallets.length === 0 && bscOptions.length > 0) {
    setupRecommendations.unshift({
      id: "binance-agentic-wallet",
      label: "Binance Agentic Wallet",
      recommended: true,
      appliesToOptionIndexes: bscOptions.map((option) => option.index),
    });
  }

  return {
    x402Version: requirements.x402Version,
    state,
    options,
    compatibleOptionIndexes: compatibleOptions.map((option) => option.index),
    selectedOptionIndex: null,
    setupRecommendations,
  };
}

export function selectPaymentOption(input, selectedIndex) {
  const options = enumeratePaymentOptions(input);
  if (!Number.isInteger(selectedIndex)) {
    fail("An explicit 1-based selected option index is required");
  }
  const option = options.find(({ index }) => index === selectedIndex);
  if (!option) fail(`Selected payment option ${selectedIndex} does not exist`);
  return option;
}

function assertEnvelopeField(actual, expected, field) {
  if (actual == null || !sameValue(actual, expected)) {
    fail(`Payment envelope ${field} does not match the selected accept`);
  }
}

export function normalizePaymentEnvelope(envelopeInput, requirementsInput, selectedIndex) {
  const requirements = parsePaymentRequirements(requirementsInput);
  const selected = selectPaymentOption(requirements, selectedIndex);
  const envelope =
    typeof envelopeInput === "string"
      ? decodeBase64Json(envelopeInput, "payment envelope")
      : structuredClone(envelopeInput);

  if (!isObject(envelope)) fail("Payment envelope must be an object");
  assertEnvelopeField(
    envelope.x402Version,
    requirements.x402Version,
    "x402Version"
  );

  const accepted = envelope.accepted;
  if (accepted != null) {
    if (!isObject(accepted)) fail("Payment envelope accepted must be an object");
    for (const field of ["scheme", "network", "asset", "amount", "payTo"]) {
      assertEnvelopeField(accepted[field], selected[field], `accepted.${field}`);
    }
  }

  if (!isObject(envelope.payload)) fail("Payment envelope is missing payload");
  if (!envelope.payload.signature) fail("Payment envelope is missing signature");
  const authorization = envelope.payload.authorization;
  if (!isObject(authorization)) {
    fail("Payment envelope is missing authorization");
  }
  assertEnvelopeField(authorization.to, selected.payTo, "authorization.to");
  assertEnvelopeField(authorization.value, selected.amount, "authorization.value");
  for (const field of ["from", "validAfter", "validBefore", "nonce"]) {
    if (authorization[field] == null || String(authorization[field]) === "") {
      fail(`Payment envelope authorization is missing ${field}`);
    }
  }

  return {
    x402Version: requirements.x402Version,
    scheme: selected.scheme,
    network: selected.network,
    payload: structuredClone(envelope.payload),
  };
}

export function buildPaymentHeader(envelope, requirements, selectedIndex) {
  const normalized = normalizePaymentEnvelope(
    envelope,
    requirements,
    selectedIndex
  );
  return Buffer.from(JSON.stringify(normalized), "utf8").toString("base64");
}

export function assertUnusedNonce(nonce, usedNonces) {
  if (typeof nonce !== "string" || nonce === "") fail("Nonce is required");
  if (!(usedNonces instanceof Set)) fail("usedNonces must be a Set");
  if (usedNonces.has(nonce)) fail("Nonce has already been used");
  usedNonces.add(nonce);
}

export function assertSameProbabilityRequest(original, replay) {
  if (JSON.stringify(original) !== JSON.stringify(replay)) {
    fail("Paid replay must use the exact original probability request body");
  }
}
