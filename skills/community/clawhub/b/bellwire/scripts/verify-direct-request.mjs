// SPDX-License-Identifier: MIT-0

const MAX_CLOCK_SKEW_SECONDS = 300;

export async function verifyBellwireDirectRequest(request, options) {
  const connectionId = request.headers.get("x-bellwire-connection");
  const keyId = request.headers.get("x-bellwire-key-id");
  const timestamp = request.headers.get("x-bellwire-timestamp");
  const nonce = request.headers.get("x-bellwire-nonce");
  const encodedSignature = request.headers.get("x-bellwire-signature");
  if (
    connectionId !== options.connectionId
    || keyId !== options.keyId
    || !/^\d{10}$/u.test(timestamp ?? "")
    || !nonce
    || nonce.length > 120
    || !encodedSignature
  ) {
    return false;
  }

  const nowSeconds = Math.floor((options.now?.() ?? Date.now()) / 1_000);
  const requestSeconds = Number(timestamp);
  if (Math.abs(nowSeconds - requestSeconds) > MAX_CLOCK_SKEW_SECONDS) return false;

  const url = new URL(request.url);
  const target = `${url.pathname}${url.search}`;
  const body = request.method === "GET" || request.method === "HEAD"
    ? new Uint8Array()
    : new Uint8Array(await request.clone().arrayBuffer());
  const bodyHash = hex(await crypto.subtle.digest("SHA-256", body));
  const canonical = [
    request.method.toUpperCase(),
    target,
    timestamp,
    nonce,
    bodyHash,
  ].join("\n");

  try {
    const publicKey = await crypto.subtle.importKey(
      "raw",
      decodeBase64(options.signingPublicKey),
      { name: "ECDSA", namedCurve: "P-256" },
      false,
      ["verify"],
    );
    const valid = await crypto.subtle.verify(
      { name: "ECDSA", hash: "SHA-256" },
      publicKey,
      decodeBase64(encodedSignature),
      new TextEncoder().encode(canonical),
    );
    if (!valid) return false;
  } catch {
    return false;
  }

  return options.consumeNonce
    ? await options.consumeNonce(`${keyId}:${nonce}`, requestSeconds)
    : true;
}

function decodeBase64(value) {
  const binary = atob(value);
  return Uint8Array.from(binary, (character) => character.charCodeAt(0));
}

function hex(value) {
  return [...new Uint8Array(value)]
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}
