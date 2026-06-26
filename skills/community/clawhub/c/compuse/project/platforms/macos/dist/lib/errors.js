export function errorMessage(error) {
    if (error instanceof Error)
        return error.message;
    return String(error);
}
export function getErrnoCode(error) {
    if (typeof error === 'object' && error !== null && 'code' in error) {
        const code = error.code;
        return typeof code === 'string' ? code : undefined;
    }
    return undefined;
}
//# sourceMappingURL=errors.js.map