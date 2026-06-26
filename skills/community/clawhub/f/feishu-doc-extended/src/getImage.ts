async function getImage(client: Lark.Client, imageToken: string) {
  const domain = client.domain ?? "https://open.feishu.cn";
  const token = await client.tokenManager.getTenantAccessToken();

  const res = await client.httpInstance.get<{ code?: number; data?: { image_url?: string } }>(
    `${domain}/open-apis/image/v4/get`,
    {
      params: { image_token: imageToken },
      headers: { Authorization: `Bearer ${token}` },
    },
  );

  if (res.data?.code !== 0 && res.data?.code !== undefined) {
    throw new Error(`Failed to get image: ${res.data}`);
  }

  return {
    image_url: res.data?.data?.image_url,
    image_token: imageToken,
  };
}

// ============ Actions ============

const STRUCTURED_BLOCK_TYPES = new Set([14, 18, 21, 23, 27, 30, 31, 32]);

async function readDoc(client: Lark.Client, docToken: string) {
  const [contentRes, infoRes, blocksRes] = await Promise.all([
    client.docx.document.rawContent({ path: { document_id: docToken } }),
    client.docx.document.get({ path: { document_id: docToken } }),
    client.docx.documentBlock.list({ path: { document_id: docToken } }),
