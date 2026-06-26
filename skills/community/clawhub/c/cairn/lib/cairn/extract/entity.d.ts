import type { ExtractedEdge, ExtractedEntity, ExtractedFile, PerFileForEdges } from '../types/extract.types.js';
export declare const extractFromFile: (content: string, filePath: string) => ExtractedFile;
export declare const buildCrossSourceEdges: (perFile: PerFileForEdges[], external: Map<string, ExtractedEntity>) => ExtractedEdge[];
export declare const buildCrossFileEdges: (perFile: PerFileForEdges[]) => ExtractedEdge[];
export declare const buildEdges: (file: PerFileForEdges) => ExtractedEdge[];
