import type { PdfExtraction } from './types/pdf.types.js';
export declare const extractPdfText: (buffer: Buffer | Uint8Array) => Promise<PdfExtraction>;
