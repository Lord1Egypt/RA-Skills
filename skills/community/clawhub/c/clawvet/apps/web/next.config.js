/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  transpilePackages: ["@clawvet/shared"],
};

module.exports = nextConfig;
