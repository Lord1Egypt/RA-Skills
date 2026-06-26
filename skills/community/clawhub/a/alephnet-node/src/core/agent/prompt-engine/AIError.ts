export class AIError extends Error {
    constructor(message: string, public details?: any) {
        super(message);
        this.name = 'AIError';
    }
}
