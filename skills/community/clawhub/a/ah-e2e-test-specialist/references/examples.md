# E2e Test Specialist — Code Examples

## Example 1

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'results.xml' }],
    ['allure-playwright']
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});

// tests/utils/base-page.ts
import { Page, Locator, expect } from '@playwright/test';

export class BasePage {
  readonly page: Page;
  readonly url: string;

  constructor(page: Page, url: string = '') {
    this.page = page;
    this.url = url;
  }

  async goto() {
    await this.page.goto(this.url);
    await this.waitForPageLoad();
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForLoadState('domcontentloaded');
  }

  async waitForElement(selector: string, timeout: number = 30000) {
    return await this.page.waitForSelector(selector, { timeout });
  }

  async scrollToElement(locator: Locator) {
    await locator.scrollIntoViewIfNeeded();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ 
      path: `screenshots/${name}.png`,
      fullPage: true 
    });
  }

  async expectToBeVisible(locator: Locator) {
    await expect(locator).toBeVisible();
  }

  async expectToHaveText(locator: Locator, text: string) {
    await expect(locator).toHaveText(text);
  }

  async expectToHaveUrl(url: string | RegExp) {
    await expect(this.page).toHaveURL(url);
  }
}

// tests/pages/login-page.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from '../utils/base-page';

export class LoginPage extends BasePage {
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    super(page, '/login');
    this.usernameInput = page.getByTestId('username-input');
    this.passwordInput = page.getByTestId('password-input');
    this.loginButton = page.getByTestId('login-button');
    this.errorMessage = page.getByTestId('error-message');
    this.forgotPasswordLink = page.getByTestId('forgot-password-link');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async loginWithValidCredentials() {
    await this.login('test@example.com', 'password123');
    await this.page.waitForURL('/dashboard');
  }

  async expectLoginError(message: string) {
    await this.expectToBeVisible(this.errorMessage);
    await this.expectToHaveText(this.errorMessage, message);
  }
}

// tests/e2e/authentication.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login-page';
import { DashboardPage } from '../pages/dashboard-page';

test.describe('Authentication', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    await loginPage.goto();
  });

  test('should login with valid credentials', async ({ page }) => {
    await loginPage.loginWithValidCredentials();
    await dashboardPage.expectToBeDashboard();
    await expect(page).toHaveURL('/dashboard');
  });

  test('should show error for invalid credentials', async () => {
    await loginPage.login('invalid@example.com', 'wrongpassword');
    await loginPage.expectLoginError('Invalid username or password');
  });

  test('should redirect to forgot password page', async ({ page }) => {
    await loginPage.forgotPasswordLink.click();
    await expect(page).toHaveURL('/forgot-password');
  });

  test('should prevent access to protected routes when not authenticated', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/login');
  });
});
```

## Example 2

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    chromeWebSecurity: false,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    setupNodeEvents(on, config) {
      // Task plugins
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },
        queryDb: (query) => {
          return queryDatabase(query, config);
        },
        seedDatabase: () => {
          return seedTestDatabase(config);
        }
      });

      // Code coverage
      require('@cypress/code-coverage/task')(on, config);
      
      return config;
    },
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
  },
});

// cypress/support/commands.ts
declare global {
  namespace Cypress {
    interface Chainable {
      login(username?: string, password?: string): Chainable<void>;
      logout(): Chainable<void>;
      createUser(userData: any): Chainable<void>;
      seedTestData(): Chainable<void>;
      waitForApiCall(alias: string): Chainable<void>;
      checkAccessibility(): Chainable<void>;
    }
  }
}

Cypress.Commands.add('login', (username = 'test@example.com', password = 'password123') => {
  cy.session([username, password], () => {
    cy.visit('/login');
    cy.get('[data-testid="username-input"]').type(username);
    cy.get('[data-testid="password-input"]').type(password);
    cy.get('[data-testid="login-button"]').click();
    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="user-menu"]').should('be.visible');
  });
});

Cypress.Commands.add('logout', () => {
  cy.get('[data-testid="user-menu"]').click();
  cy.get('[data-testid="logout-button"]').click();
  cy.url().should('include', '/login');
});

Cypress.Commands.add('createUser', (userData) => {
  cy.request({
    method: 'POST',
    url: '/api/users',
    body: userData,
    headers: {
      'Authorization': `Bearer ${Cypress.env('API_TOKEN')}`
    }
  }).then((response) => {
    expect(response.status).to.eq(201);
  });
});

Cypress.Commands.add('seedTestData', () => {
  cy.task('seedDatabase');
});

Cypress.Commands.add('waitForApiCall', (alias) => {
  cy.wait(alias).then((interception) => {
    expect(interception.response?.statusCode).to.be.oneOf([200, 201, 204]);
  });
});

Cypress.Commands.add('checkAccessibility', () => {
  cy.injectAxe();
  cy.checkA11y(null, {
    rules: {
      'color-contrast': { enabled: true },
      'keyboard-navigation': { enabled: true }
    }
  });
});

// cypress/e2e/user-management.cy.ts
describe('User Management', () => {
  beforeEach(() => {
    cy.seedTestData();
    cy.login();
    cy.visit('/admin/users');
  });

  it('should display user list', () => {
    cy.intercept('GET', '/api/users*', { fixture: 'users.json' }).as('getUsers');
    
    cy.get('[data-testid="users-table"]').should('be.visible');
    cy.waitForApiCall('@getUsers');
    
    cy.get('[data-testid="user-row"]').should('have.length.at.least', 1);
    cy.get('[data-testid="user-email"]').first().should('contain', '@');
  });

  it('should create new user', () => {
    cy.intercept('POST', '/api/users', { statusCode: 201, body: { id: 123 } }).as('createUser');
    
    cy.get('[data-testid="add-user-button"]').click();
    cy.get('[data-testid="user-form-modal"]').should('be.visible');
    
    // Fill form
    cy.get('[data-testid="first-name-input"]').type('John');
    cy.get('[data-testid="last-name-input"]').type('Doe');
    cy.get('[data-testid="email-input"]').type('john.doe@example.com');
    cy.get('[data-testid="role-select"]').select('user');
    
    cy.get('[data-testid="save-user-button"]').click();
    
    cy.waitForApiCall('@createUser');
    cy.get('[data-testid="success-message"]').should('contain', 'User created successfully');
  });

  it('should handle form validation errors', () => {
    cy.get('[data-testid="add-user-button"]').click();
    cy.get('[data-testid="save-user-button"]').click();
    
    cy.get('[data-testid="first-name-error"]').should('contain', 'First name is required');
    cy.get('[data-testid="email-error"]').should('contain', 'Email is required');
  });

  it('should filter users by role', () => {
    cy.get('[data-testid="role-filter"]').select('admin');
    
    cy.get('[data-testid="user-row"]').each(($row) => {
      cy.wrap($row).find('[data-testid="user-role"]').should('contain', 'admin');
    });
  });
});
```

## Example 3

```typescript
// tests/api/user-api.spec.ts
import { test, expect } from '@playwright/test';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3001/api';

test.describe('User API', () => {
  let authToken: string;
  let userId: number;

  test.beforeAll(async ({ request }) => {
    // Get auth token
    const loginResponse = await request.post(`${API_BASE_URL}/auth/login`, {
      data: {
        email: 'admin@example.com',
        password: 'admin123'
      }
    });
    
    expect(loginResponse.ok()).toBeTruthy();
    const loginData = await loginResponse.json();
    authToken = loginData.token;
  });

  test('should create user via API', async ({ request }) => {
    const userData = {
      firstName: 'API',
      lastName: 'User',
      email: `api-user-${Date.now()}@example.com`,
      role: 'user'
    };

    const response = await request.post(`${API_BASE_URL}/users`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      data: userData
    });

    expect(response.ok()).toBeTruthy();
    
    const responseData = await response.json();
    expect(responseData).toHaveProperty('id');
    expect(responseData.email).toBe(userData.email);
    
    userId = responseData.id;
  });

  test('should get user by ID', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    expect(response.ok()).toBeTruthy();
    
    const userData = await response.json();
    expect(userData.id).toBe(userId);
    expect(userData).toHaveProperty('firstName');
    expect(userData).toHaveProperty('lastName');
  });

  test('should update user', async ({ request }) => {
    const updateData = {
      firstName: 'Updated',
      lastName: 'Name'
    };

    const response = await request.patch(`${API_BASE_URL}/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      data: updateData
    });

    expect(response.ok()).toBeTruthy();
    
    const updatedUser = await response.json();
    expect(updatedUser.firstName).toBe('Updated');
    expect(updatedUser.lastName).toBe('Name');
  });

  test('should handle validation errors', async ({ request }) => {
    const invalidData = {
      firstName: '',
      email: 'invalid-email'
    };

    const response = await request.post(`${API_BASE_URL}/users`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      data: invalidData
    });

    expect(response.status()).toBe(400);
    
    const errorData = await response.json();
    expect(errorData).toHaveProperty('errors');
    expect(errorData.errors).toContain('First name is required');
    expect(errorData.errors).toContain('Invalid email format');
  });

  test.afterAll(async ({ request }) => {
    // Cleanup: delete created user
    if (userId) {
      await request.delete(`${API_BASE_URL}/users/${userId}`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });
    }
  });
});
```

## Example 4

```typescript
// tests/visual/visual-regression.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage screenshot comparison', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Hide dynamic content
    await page.addStyleTag({
      content: `
        .timestamp, .live-data, .random-id { visibility: hidden !important; }
      `
    });
    
    await expect(page).toHaveScreenshot('homepage.png');
  });

  test('login page responsive design', async ({ page }) => {
    await page.goto('/login');
    
    // Desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('login-desktop.png');
    
    // Tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('login-tablet.png');
    
    // Mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('login-mobile.png');
  });

  test('component screenshot with different states', async ({ page }) => {
    await page.goto('/components/button');
    
    const button = page.getByTestId('primary-button');
    
    // Default state
    await expect(button).toHaveScreenshot('button-default.png');
    
    // Hover state
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');
    
    // Focus state
    await button.focus();
    await expect(button).toHaveScreenshot('button-focus.png');
    
    // Disabled state
    await page.evaluate(() => {
      document.querySelector('[data-testid="primary-button"]')?.setAttribute('disabled', 'true');
    });
    await expect(button).toHaveScreenshot('button-disabled.png');
  });
});

// tests/accessibility/a11y.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('should not have accessibility violations on homepage', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should be keyboard navigable', async ({ page }) => {
    await page.goto('/');
    
    // Test tab navigation
    await page.keyboard.press('Tab');
    await expect(page.getByTestId('main-nav')).toBeFocused();
    
    await page.keyboard.press('Tab');
    await expect(page.getByTestId('search-input')).toBeFocused();
    
    await page.keyboard.press('Tab');
    await expect(page.getByTestId('user-menu')).toBeFocused();
  });

  test('should have proper ARIA labels and roles', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Check for proper headings hierarchy
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
    expect(headings.length).toBeGreaterThan(0);
    
    // Check for form labels
    const formInputs = await page.locator('input[type="text"], input[type="email"], textarea, select').all();
    for (const input of formInputs) {
      const ariaLabel = await input.getAttribute('aria-label');
      const associatedLabel = await page.locator(`label[for="${await input.getAttribute('id')}"]`).count();
      
      expect(ariaLabel || associatedLabel > 0).toBeTruthy();
    }
  });

  test('should support screen reader navigation', async ({ page }) => {
    await page.goto('/products');
    
    // Check for skip links
    await expect(page.getByTestId('skip-to-content')).toBeHidden();
    await page.keyboard.press('Tab');
    await expect(page.getByTestId('skip-to-content')).toBeVisible();
    
    // Check for landmark regions
    await expect(page.locator('main[role="main"]')).toBeVisible();
    await expect(page.locator('nav[role="navigation"]')).toBeVisible();
    await expect(page.locator('aside[role="complementary"]')).toBeVisible();
  });
});
```

## Example 5

```typescript
// tests/fixtures/test-data.ts
import { faker } from '@faker-js/faker';

export interface User {
  id?: number;
  firstName: string;
  lastName: string;
  email: string;
  role: 'admin' | 'user' | 'moderator';
  isActive: boolean;
  createdAt?: string;
}

export interface Product {
  id?: number;
  name: string;
  description: string;
  price: number;
  category: string;
  inStock: boolean;
  imageUrl?: string;
}

export class TestDataFactory {
  static createUser(overrides: Partial<User> = {}): User {
    return {
      firstName: faker.person.firstName(),
      lastName: faker.person.lastName(),
      email: faker.internet.email(),
      role: faker.helpers.arrayElement(['admin', 'user', 'moderator']),
      isActive: faker.datatype.boolean(),
      ...overrides
    };
  }

  static createUsers(count: number, overrides: Partial<User> = {}): User[] {
    return Array.from({ length: count }, () => this.createUser(overrides));
  }

  static createProduct(overrides: Partial<Product> = {}): Product {
    return {
      name: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      price: parseFloat(faker.commerce.price()),
      category: faker.commerce.department(),
      inStock: faker.datatype.boolean(),
      imageUrl: faker.image.url(),
      ...overrides
    };
  }

  static createAdminUser(): User {
    return this.createUser({
      role: 'admin',
      isActive: true,
      email: 'admin@example.com'
    });
  }

  static createTestScenarios() {
    return {
      validLoginCredentials: {
        username: 'test@example.com',
        password: 'password123'
      },
      invalidLoginCredentials: {
        username: 'invalid@example.com',
        password: 'wrongpassword'
      },
      productCatalog: this.createProducts(10),
      userList: this.createUsers(5)
    };
  }

  static createProducts(count: number): Product[] {
    return Array.from({ length: count }, () => this.createProduct());
  }
}

// tests/utils/database-helpers.ts
import { Pool } from 'pg';

export class DatabaseHelper {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      database: process.env.DB_NAME || 'test_db',
      user: process.env.DB_USER || 'test_user',
      password: process.env.DB_PASSWORD || 'test_password'
    });
  }

  async seedDatabase() {
    const client = await this.pool.connect();
    
    try {
      // Clear existing data
      await client.query('TRUNCATE TABLE users, products, orders CASCADE');
      
      // Insert test users
      const users = TestDataFactory.createUsers(10);
      for (const user of users) {
        await client.query(
          'INSERT INTO users (first_name, last_name, email, role, is_active) VALUES ($1, $2, $3, $4, $5)',
          [user.firstName, user.lastName, user.email, user.role, user.isActive]
        );
      }

      // Insert test products
      const products = TestDataFactory.createProducts(20);
      for (const product of products) {
        await client.query(
          'INSERT INTO products (name, description, price, category, in_stock) VALUES ($1, $2, $3, $4, $5)',
          [product.name, product.description, product.price, product.category, product.inStock]
        );
      }
      
    } finally {
      client.release();
    }
  }

  async cleanupDatabase() {
    const client = await this.pool.connect();
    
    try {
      await client.query('TRUNCATE TABLE users, products, orders CASCADE');
    } finally {
      client.release();
    }
  }

  async getUserByEmail(email: string) {
    const client = await this.pool.connect();
    
    try {
      const result = await client.query('SELECT * FROM users WHERE email = $1', [email]);
      return result.rows[0];
    } finally {
      client.release();
    }
  }

  async close() {
    await this.pool.end();
  }
}
```

## Example 6

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Run nightly at 2 AM

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Setup test database
      run: |
        docker run -d \
          --name test-db \
          -e POSTGRES_DB=test_db \
          -e POSTGRES_USER=test_user \
          -e POSTGRES_PASSWORD=test_password \
          -p 5432:5432 \
          postgres:13
        
        # Wait for database to be ready
        sleep 10
        npm run db:migrate
    
    - name: Start application
      run: |
        npm run build
        npm start &
        npx wait-on http://localhost:3000
    
    - name: Install Playwright browsers
      run: npx playwright install --with-deps ${{ matrix.browser }}
    
    - name: Run E2E tests
      run: npx playwright test --project=${{ matrix.browser }}
      env:
        BASE_URL: http://localhost:3000
        DB_HOST: localhost
        DB_PORT: 5432
        DB_NAME: test_db
        DB_USER: test_user
        DB_PASSWORD: test_password
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: playwright-report-${{ matrix.browser }}
        path: playwright-report/
        retention-days: 30
    
    - name: Upload screenshots
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: screenshots-${{ matrix.browser }}
        path: test-results/
        retention-days: 30

  visual-regression:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Start application
      run: |
        npm run build
        npm start &
        npx wait-on http://localhost:3000
    
    - name: Run visual regression tests
      run: npx playwright test tests/visual/
    
    - name: Upload visual diffs
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: visual-diffs
        path: test-results/
        retention-days: 30

  accessibility-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Start application
      run: |
        npm run build
        npm start &
        npx wait-on http://localhost:3000
    
    - name: Run accessibility tests
      run: npx playwright test tests/accessibility/
    
    - name: Generate accessibility report
      run: |
        npm run a11y:report
        
    - name: Upload accessibility report
      uses: actions/upload-artifact@v3
      with:
        name: accessibility-report
        path: accessibility-report/
        retention-days: 30
```

## Example 7

```typescript
// tests/performance/performance.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  test('page load performance', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/', { waitUntil: 'networkidle' });
    
    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(3000); // 3 seconds max
    
    // Measure Core Web Vitals
    const vitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const vitals: Record<string, number> = {};
          
          entries.forEach((entry) => {
            if (entry.name === 'first-contentful-paint') {
              vitals.fcp = entry.startTime;
            }
            if (entry.name === 'largest-contentful-paint') {
              vitals.lcp = entry.startTime;
            }
          });
          
          resolve(vitals);
        }).observe({ type: 'largest-contentful-paint', buffered: true });
      });
    });
    
    expect(vitals.lcp).toBeLessThan(2500); // Good LCP threshold
  });

  test('API response times', async ({ request }) => {
    const start = Date.now();
    
    const response = await request.get('/api/users');
    
    const responseTime = Date.now() - start;
    
    expect(response.ok()).toBeTruthy();
    expect(responseTime).toBeLessThan(500); // 500ms max
  });
});
```
