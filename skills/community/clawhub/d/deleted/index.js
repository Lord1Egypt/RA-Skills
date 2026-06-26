export default async function BeeLanguagesGet(args = {}) {
    const API_KEY = args.api_key;

    if (!API_KEY) {
        return {
            status: false,
            msg: "Missing API_KEY. Please obtain it from the developer platform at https://open.tradew.com before use."
        };
    }

    try {
        const response = await fetch("https://platform.tradew.com/openapis/languages", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${API_KEY}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("HTTP ERROR");
        }

        return await response.json();

    } catch (error) {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
