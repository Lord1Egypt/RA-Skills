export default async function BeeVisitorRecent(args = {}) {
    const API_KEY = args.api_key;

    if (!API_KEY) {
        return {
            status: false,
            msg: "Missing API_KEY. Please obtain it from the developer platform at https://open.tradew.com before use."
        };
    }

    const current_page = Number(args.current_page ?? 1);
    const page_size = Number(args.page_size ?? 10);

    if (page_size < 10 || page_size > 50) {
        return {
            status: false,
            msg: "page_size must be between 10 and 50."
        };
    }

    const body = {
        pagination: {
            current_page,
            page_size
        }
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/visitor/recent",
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${API_KEY}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(body)
            }
        );

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
