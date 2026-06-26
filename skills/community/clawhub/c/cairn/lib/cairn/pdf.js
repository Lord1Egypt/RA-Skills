// PDF text extraction. unpdf wraps Mozilla's pdf.js for server-side use; we
// pull the merged-pages text and let the existing text chunker handle layout.
// Page-level metadata (page numbers per chunk) is intentionally not preserved
// — chunk start/end lines are line indices in the joined text, consistent
// with how `kind: 'web'` and `kind: 'text'` already behave.
import { extractText, getDocumentProxy } from 'unpdf';
export const extractPdfText = async (buffer) => {
    // pdfjs explicitly rejects Buffer (a Uint8Array subclass in Node) and
    // demands a plain Uint8Array. Re-wrap zero-copy via the underlying
    // ArrayBuffer; Buffer.subarray's view is preserved.
    const data = buffer instanceof Buffer
        ? new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
        : buffer;
    const doc = await getDocumentProxy(data);
    const { text, totalPages } = await extractText(doc, { mergePages: true });
    return { text, pages: totalPages };
};
