export const websiteTools = [
  { name: "list_websites", description: "List websites", inputSchema: { type: "object", properties: {} } },
  { name: "create_website", description: "Create website", inputSchema: { type: "object", properties: { site: { type: "object" } }, required: ["site"] } },
  { name: "get_website", description: "Get website details", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_website", description: "Update website", inputSchema: { type: "object", properties: { site: { type: "object" } }, required: ["site"] } },
  { name: "delete_website", description: "Delete website", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "list_website_domains", description: "List website domains", inputSchema: { type: "object", properties: { websiteId: { type: "number" } }, required: ["websiteId"] } },
  { name: "create_website_domain", description: "Add domain to website", inputSchema: { type: "object", properties: { websiteId: { type: "number" }, domain: { type: "string" }, port: { type: "number" } }, required: ["websiteId", "domain"] } },
  { name: "delete_website_domain", description: "Remove domain from website", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_website_domain", description: "Update website domain", inputSchema: { type: "object", properties: { id: { type: "number" }, websiteId: { type: "number" }, domain: { type: "string" }, port: { type: "number" } }, required: ["id", "websiteId"] } },
  { name: "list_certificates", description: "List SSL certificates", inputSchema: { type: "object", properties: {} } },
  { name: "get_certificate", description: "Get SSL certificate details", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "create_certificate", description: "Create SSL certificate", inputSchema: { type: "object", properties: { cert: { type: "object" } }, required: ["cert"] } },
  { name: "delete_certificate", description: "Delete SSL certificate", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "obtain_ssl", description: "Obtain SSL certificate (Let's Encrypt)", inputSchema: { type: "object", properties: { ID: { type: "number" }, domains: { type: "array", items: { type: "string" } }, keyType: { type: "string" }, time: { type: "number" }, unit: { type: "string" }, autoRenew: { type: "boolean" } }, required: ["ID", "domains", "keyType"] } },
  { name: "renew_ssl", description: "Renew SSL certificate", inputSchema: { type: "object", properties: { ID: { type: "number" } }, required: ["ID"] } },
  { name: "resolve_ssl", description: "Resolve SSL certificate", inputSchema: { type: "object", properties: { websiteSSLId: { type: "number" } }, required: ["websiteSSLId"] } },
  { name: "upload_ssl", description: "Upload SSL certificate", inputSchema: { type: "object", properties: { cert: { type: "object" } }, required: ["cert"] } },
  { name: "get_website_ssl", description: "Get website SSL certificate", inputSchema: { type: "object", properties: { websiteId: { type: "number" } }, required: ["websiteId"] } },
  { name: "get_https", description: "Get HTTPS configuration", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_https", description: "Update HTTPS configuration", inputSchema: { type: "object", properties: { websiteId: { type: "number" }, type: { type: "string" }, enable: { type: "boolean" }, httpConfig: { type: "string" }, privateKey: { type: "string" }, certificate: { type: "string" }, algorithm: { type: "string" }, hsts: { type: "boolean" }, hstsIncludeSubDomains: { type: "boolean" }, http3: { type: "boolean" }, httpsPorts: { type: "array", items: { type: "number" } } }, required: ["websiteId", "type", "enable"] } },
  { name: "apply_ssl", description: "Apply SSL to website", inputSchema: { type: "object", properties: { websiteId: { type: "number" }, websiteSSLId: { type: "number" }, type: { type: "string" }, enable: { type: "boolean" }, httpConfig: { type: "string" }, privateKey: { type: "string" }, certificate: { type: "string" } }, required: ["websiteId", "type", "enable"] } },
  { name: "get_nginx_conf", description: "Get Nginx configuration", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_nginx_conf", description: "Update Nginx configuration", inputSchema: { type: "object", properties: { id: { type: "number" }, content: { type: "string" } }, required: ["id", "content"] } },
];

export async function handleWebsiteTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_websites": return await client.listWebsites();
    case "create_website": return await client.createWebsite(args?.site);
    case "get_website": return await client.getWebsite(args?.id);
    case "update_website": return await client.updateWebsite(args?.site);
    case "delete_website": return await client.deleteWebsite(args?.id);
    case "list_website_domains": return await client.listWebsiteDomains(args?.websiteId);
    case "create_website_domain": return await client.createWebsiteDomain(args);
    case "delete_website_domain": return await client.deleteWebsiteDomain(args);
    case "update_website_domain": return await client.updateWebsiteDomain(args);
    case "list_certificates": return await client.listCertificates();
    case "get_certificate": return await client.getCertificate(args?.id);
    case "create_certificate": return await client.createCertificate(args?.cert);
    case "delete_certificate": return await client.deleteCertificate(args?.id);
    case "obtain_ssl": return await client.obtainSSL(args);
    case "renew_ssl": return await client.renewSSL(args);
    case "resolve_ssl": return await client.resolveSSL(args);
    case "upload_ssl": return await client.uploadSSL(args);
    case "get_website_ssl": return await client.getWebsiteSSL(args?.websiteId);
    case "get_https": return await client.getHTTPS(args?.id);
    case "update_https": return await client.updateHTTPS(args);
    case "apply_ssl": return await client.applySSL(args);
    case "get_nginx_conf": return await client.getNginxConf(args?.id);
    case "update_nginx_conf": return await client.updateNginxConf(args);
    case "get_antileech_conf": return await client.getAntiLeechConf(args?.websiteId);
    case "update_antileech": return await client.updateAntiLeech(args?.params);
    default: return null;
  }
}
