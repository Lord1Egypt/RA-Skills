# js-srp-gsa

This is a fork of [`js-srp`](https://github.com/jchv/js-srp) that adds support for the variant of SRP used by Apple icloud.com.

## Example usage

### SRP wrapper
```ts
import { Client, Hash, Mode, Srp, util } from "@foxt/js-srp";
import crypto from "crypto";

export type SRPProtocol = "s2k" | "s2k_fo";

export interface ServerSRPInitRequest {
    a: string;
    accountName: string;
    protocols: SRPProtocol[];
}
export interface ServerSRPInitResponse {
    iteration: number;
    salt: string;
    protocol: "s2k" | "s2k_fo";
    b: string;
    c: string;
}
export interface ServerSRPCompleteRequest {
    accountName: string;
    c: string;
    m1: string;
    m2: string;
    rememberMe: boolean;
    trustTokens: string[];
}

let srp = new Srp(Mode.GSA, Hash.SHA256, 2048);
const stringToU8Array = (str: string) => new TextEncoder().encode(str);
const base64ToU8Array = (str: string) => Uint8Array.from(Buffer.from(str, "base64"));
export class GSASRPAuthenticator {
    constructor(private username: string) { }
    private srpClient?: Client = undefined;


    private async derivePassword(protocol: "s2k" | "s2k_fo", password: string, salt: Uint8Array, iterations: number) {
        let passHash = new Uint8Array(await util.hash(srp.h, stringToU8Array(password)));
        if (protocol == "s2k_fo") {
            passHash = stringToU8Array(util.toHex(passHash));
        }

        let imported = await crypto.subtle.importKey(
            "raw",
            passHash,
            { name: "PBKDF2" },
            false,
            ["deriveBits"]
        );
        let derived = await crypto.subtle.deriveBits({
            name: "PBKDF2",
            hash: { name: "SHA-256" },
            iterations, salt
        }, imported, 256);

        return new Uint8Array(derived);
    }


    async getInit(): Promise<ServerSRPInitRequest> {
        if (this.srpClient) throw new Error("Already initialized");
        this.srpClient = await srp.newClient(
            stringToU8Array(this.username),
            // provide fake passsword because we need to get data from server
            new Uint8Array()
        );
        let a = Buffer.from(
            util.bytesFromBigint(this.srpClient.A)
        ).toString("base64");
        return {
            a, protocols: ["s2k", "s2k_fo"],
            accountName: this.username,
        };
    }
    async getComplete(password: string, serverData: ServerSRPInitResponse): Promise<Pick<ServerSRPCompleteRequest, "m1" | "m2" | "c" | "accountName">> {
        if (!this.srpClient) throw new Error("Not initialized");
        if ((serverData.protocol != "s2k") &&
            (serverData.protocol != "s2k_fo")) throw new Error("Unsupported protocol " + serverData.protocol);
        let salt = base64ToU8Array(serverData.salt);
        let serverPub = base64ToU8Array(serverData.b);
        let iterations = serverData.iteration;
        let derived = await this.derivePassword(
            serverData.protocol, password,
            salt, iterations
        );
        this.srpClient.p = derived;
        await this.srpClient.generate(salt, serverPub);
        let m1 = Buffer.from(this.srpClient._M).toString("base64");
        let M2 = await this.srpClient.generateM2();
        let m2 = Buffer.from(M2).toString("base64");
        return {
            accountName: this.username,
            m1,
            m2,
            c: serverData.c,
        };
    }
}
```

### API interop
```ts
import prompt from "prompt";
import type { ServerSRPInitResponse } from "./GSASRPAuthenticator.js";
import { GSASRPAuthenticator } from "./GSASRPAuthenticator.js";

async function request(url: string, body: any) {
    let req = await fetch("https://idmsa.apple.com/appleauth/auth/signin" + url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        },
        body: JSON.stringify(body)
    })
    console.log()
    console.log("POST", url)
    console.log("    ", req.status, req.statusText)

    if (!req.ok) throw new Error(
        "Failed to get init response " + req.status + " " + req.statusText + ": " 
        + await req.text()
    );
    return await req.json();
}


async function login(username: string, password: string) {
    // set up SRP authenticator & get public key
    let authenticator = new GSASRPAuthenticator(username);
    let initData = await authenticator.getInit();

    // request SRP init data from server
    let initResp = await request("/init", initData)
    

    // get proof of password
    let proof = await authenticator.getComplete(password, initResp as ServerSRPInitResponse);

    // send proof to server
    let completeResp = await request("/complete", {
            ...proof,
            rememberMe: true,
            trustTokens: []
    })
    console.log(completeResp)

    
}
prompt.start();
prompt.get({
    properties: {
        username: {
            description: "Apple ID"
        },
        password: {
            description: "Password",
            hidden: true
        }
    }
}, (err, result) => {
    if (err) return console.error(err);
    login(result.username as string, result.password as string).catch(console.error);
})


```