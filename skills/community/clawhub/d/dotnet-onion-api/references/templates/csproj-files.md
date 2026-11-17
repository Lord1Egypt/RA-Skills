# `.csproj` templates

⚠️ **Do not paste these as-is.** The `<TargetFramework>` and every `<PackageReference Version="…">` must be resolved at scaffold time (see SKILL.md Step 1). Treat the version strings here as placeholders shown for shape only.

## `Directory.Build.props` (solution root)

```xml
<Project>
  <PropertyGroup>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <EnableNETAnalyzers>true</EnableNETAnalyzers>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
  </PropertyGroup>
</Project>
```

## `src/{{Solution}}.Domain/{{Solution}}.Domain.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>{{TFM}}</TargetFramework>
  </PropertyGroup>
  <!-- ZERO ProjectReferences. Domain depends on nothing. -->
</Project>
```

## `src/{{Solution}}.Application/{{Solution}}.Application.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>{{TFM}}</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\{{Solution}}.Domain\{{Solution}}.Domain.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="AutoMapper" Version="{{LATEST}}" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection.Abstractions" Version="{{LATEST}}" />
    <PackageReference Include="Scrutor" Version="{{LATEST}}" />
  </ItemGroup>
</Project>
```

## `src/{{Solution}}.Infrastructure/{{Solution}}.Infrastructure.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>{{TFM}}</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\{{Solution}}.Application\{{Solution}}.Application.csproj" />
    <ProjectReference Include="..\{{Solution}}.Domain\{{Solution}}.Domain.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="{{LATEST}}" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="{{LATEST}}" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="{{LATEST}}">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Microsoft.Extensions.Configuration.Abstractions" Version="{{LATEST}}" />
    <PackageReference Include="Microsoft.Extensions.Http" Version="{{LATEST}}" />
    <PackageReference Include="Microsoft.AspNetCore.Http.Abstractions" Version="{{LATEST}}" />
  </ItemGroup>
</Project>
```

## `src/{{Solution}}.Api/{{Solution}}.Api.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>{{TFM}}</TargetFramework>
    <UserSecretsId>{{NEW_GUID}}</UserSecretsId>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\{{Solution}}.Application\{{Solution}}.Application.csproj" />
    <ProjectReference Include="..\{{Solution}}.Infrastructure\{{Solution}}.Infrastructure.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="{{LATEST}}" />
    <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="{{LATEST}}" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="{{LATEST}}" />
  </ItemGroup>
</Project>
```

## `src/{{Solution}}.Workers.{{Worker}}/{{Solution}}.Workers.{{Worker}}.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk.Worker">
  <PropertyGroup>
    <TargetFramework>{{TFM}}</TargetFramework>
    <OutputType>Exe</OutputType>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\{{Solution}}.Application\{{Solution}}.Application.csproj" />
    <ProjectReference Include="..\{{Solution}}.Infrastructure\{{Solution}}.Infrastructure.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Hosting" Version="{{LATEST}}" />
    <!-- Add only the SDK clients this worker actually needs: -->
    <!-- <PackageReference Include="Azure.Messaging.ServiceBus" Version="{{LATEST}}" /> -->
    <!-- <PackageReference Include="Azure.Storage.Queues" Version="{{LATEST}}" /> -->
  </ItemGroup>
  <ItemGroup>
    <None Update="appsettings.json"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></None>
    <None Update="appsettings.Development.json"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></None>
  </ItemGroup>
</Project>
```

## `tests/{{Solution}}.UnitTests/{{Solution}}.UnitTests.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>{{TFM}}</TargetFramework>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\..\src\{{Solution}}.Application\{{Solution}}.Application.csproj" />
    <ProjectReference Include="..\..\src\{{Solution}}.Domain\{{Solution}}.Domain.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="{{LATEST}}" />
    <PackageReference Include="xunit" Version="{{LATEST}}" />
    <PackageReference Include="xunit.runner.visualstudio" Version="{{LATEST}}" />
    <PackageReference Include="NSubstitute" Version="{{LATEST}}" />
    <PackageReference Include="FluentAssertions" Version="{{LATEST}}" />
    <PackageReference Include="AutoMapper" Version="{{LATEST}}" />
  </ItemGroup>
</Project>
```

## `tests/{{Solution}}.IntegrationTests/{{Solution}}.IntegrationTests.csproj`

Only generate if the user explicitly opts in.

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>{{TFM}}</TargetFramework>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\..\src\{{Solution}}.Api\{{Solution}}.Api.csproj" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="{{LATEST}}" />
    <PackageReference Include="xunit" Version="{{LATEST}}" />
    <PackageReference Include="xunit.runner.visualstudio" Version="{{LATEST}}" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="{{LATEST}}" />
    <PackageReference Include="Testcontainers.MsSql" Version="{{LATEST}}" />
    <PackageReference Include="FluentAssertions" Version="{{LATEST}}" />
  </ItemGroup>
</Project>
```

## How to resolve `{{LATEST}}` at scaffold time

For each package, call:

```
mcp__plugin_context7_context7__resolve-library-id  →  query-docs
```

with the package id (e.g. `Microsoft.EntityFrameworkCore.SqlServer`). If context7 can't resolve, fall back to `WebFetch` of `https://www.nuget.org/packages/{Package}` and parse the latest stable version (skip pre-release unless the user opts in).

Then substitute every `{{LATEST}}` with the resolved version string before writing the `.csproj`.

State the resolved version table back to the user before writing files.
