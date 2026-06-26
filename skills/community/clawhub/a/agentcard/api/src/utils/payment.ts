interface PaymentProof {
  scheme: string;
  network: string;
  payload: {
    authorization: {
      from: string;
      to: string;
      value: string;
    };
    txHash: string;
  };
}

const tryParseJson = (value: string): unknown | undefined => {
  try {
    return JSON.parse(value);
  } catch {
    return undefined;
  }
};

export const parsePaymentHeader = (header: string): PaymentProof | null => {
  const rawJson = tryParseJson(header);
  if (rawJson) {
    return rawJson as PaymentProof;
  }

  try {
    const decoded = Buffer.from(header, "base64").toString("utf8");
    const parsed = tryParseJson(decoded);
    return (parsed as PaymentProof) ?? null;
  } catch {
    return null;
  }
};
