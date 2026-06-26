"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CloudClient = void 0;
const undici_1 = require("undici");
class CloudClient {
    endpoint;
    timeoutMs;
    logger;
    constructor(endpoint, timeoutMs, logger) {
        this.endpoint = endpoint.replace(/\/$/, "");
        this.timeoutMs = timeoutMs;
        this.logger = logger;
    }
    async match(req) {
        try {
            const { statusCode, body } = await (0, undici_1.request)(`${this.endpoint}/v1/lobsters/match`, {
                method: "POST",
                headers: { "content-type": "application/json" },
                body: JSON.stringify(req),
                headersTimeout: this.timeoutMs,
                bodyTimeout: this.timeoutMs,
            });
            if (statusCode !== 200) {
                this.logger.warn(`Cloud match returned ${statusCode}`);
                return null;
            }
            return (await body.json());
        }
        catch (err) {
            this.logger.debug(`Cloud match failed (expected on timeout/offline): ${err}`);
            return null;
        }
    }
    async contribute(req) {
        try {
            const { statusCode, body } = await (0, undici_1.request)(`${this.endpoint}/v1/lobsters/contribute`, {
                method: "POST",
                headers: { "content-type": "application/json" },
                body: JSON.stringify(req),
                headersTimeout: 5000,
                bodyTimeout: 5000,
            });
            if (statusCode !== 201 && statusCode !== 409) {
                this.logger.warn(`Cloud contribute returned ${statusCode}`);
                return null;
            }
            return (await body.json());
        }
        catch (err) {
            this.logger.warn(`Cloud contribute failed: ${err}`);
            return null;
        }
    }
    async reportFailure(req) {
        try {
            await (0, undici_1.request)(`${this.endpoint}/v1/lobsters/report_failure`, {
                method: "PUT",
                headers: { "content-type": "application/json" },
                body: JSON.stringify(req),
                headersTimeout: 3000,
                bodyTimeout: 3000,
            });
        }
        catch (err) {
            this.logger.debug(`Cloud report_failure failed: ${err}`);
        }
    }
}
exports.CloudClient = CloudClient;
